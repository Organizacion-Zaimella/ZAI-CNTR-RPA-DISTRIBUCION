"""Aplicación independiente IESS para el certificado de obligaciones patronales."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright


ADAPTER_ID = "iess"
ADAPTER_VERSION = "0.1.3-candidate"
ENTRY_PATH = "/empleador-web/pages/morapatronal/certificadoCumplimientoPublico.jsf"
IESS_HOST = "www.iess.gob.ec"
MAX_PDF_BYTES = 25 * 1024 * 1024


def valid_pdf_for_ords(path: Path) -> bool:
    """Match the PDF structure checks enforced by CNTR before upload."""
    try:
        size = path.stat().st_size
        if not path.is_file() or not 100 < size <= MAX_PDF_BYTES:
            return False
        with path.open("rb") as source:
            header = source.read(5)
            source.seek(max(0, size - 8192))
            trailer = source.read(8192)
            source.seek(0)
            contains_xref = b"startxref" in source.read(MAX_PDF_BYTES + 1)
        return header == b"%PDF-" and contains_xref and b"%%EOF" in trailer
    except OSError:
        return False


def load_context(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("portal_id") != 2 or raw.get("document_id") != 2:
        raise ValueError("documento no soportado")
    url = urlparse(str(raw["entry_url"]))
    if url.scheme != "https" or url.hostname != IESS_HOST or url.path != ENTRY_PATH:
        raise ValueError("URL de entrada no autorizada")
    if not str(raw.get("identification", "")).strip():
        raise ValueError("contexto incompleto")
    repo = Path(__file__).resolve().parents[2]
    evidence_dir = Path(raw["evidence_dir"]).resolve()
    if path.resolve().is_relative_to(repo) or evidence_dir.is_relative_to(repo):
        raise ValueError("contexto y evidencias deben permanecer fuera del repositorio")
    return {
        "url": str(raw["entry_url"]),
        "identification": str(raw["identification"]).strip(),
        "evidence_dir": evidence_dir,
        "timeout": min(120, max(15, int(raw.get("timeout_seconds", 60)))),
        "pacing": max(5.0, float(raw.get("pacing_seconds", 5))),
    }


async def _run(ctx: dict) -> dict:
    ctx["evidence_dir"].mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = None
        for channel in ("msedge", "chrome"):
            try:
                browser = await p.chromium.launch(channel=channel, headless=True)
                break
            except Exception:
                continue
        if browser is None:
            return result("ERROR", "NO_SUPPORTED_BROWSER")
        page = await browser.new_page(accept_downloads=True)
        try:
            try:
                response = await page.goto(ctx["url"], wait_until="domcontentloaded", timeout=ctx["timeout"] * 1000)
            except PlaywrightTimeoutError:
                return result("RETRYABLE", "PORTAL_NAVIGATION_TIMEOUT")
            except Exception:
                return result("RETRYABLE", "PORTAL_NAVIGATION_ERROR")
            if response and response.status in (403, 429, 451):
                return result("BLOCKED", f"HTTP_{response.status}")
            challenge = re.compile(r"captcha|altcha|no soy un robot", re.I)
            if await page.get_by_text(challenge).count():
                return result("HUMAN_REQUIRED", "PORTAL_CHALLENGE")
            field = page.get_by_role("textbox")
            button = page.get_by_role("button", name="CONSULTAR", exact=True)
            if await field.count() != 1 or await button.count() != 1:
                return result("RETRYABLE", "FORM_CONTROLS_NOT_UNIQUE")
            await page.wait_for_timeout(int(ctx["pacing"] * 1000))
            await field.fill(ctx["identification"], timeout=ctx["timeout"] * 1000)
            await page.wait_for_timeout(int(ctx["pacing"] * 1000))
            if not await button.is_enabled():
                return result("RETRYABLE", "QUERY_NOT_ENABLED")

            popups = []
            page.on("popup", lambda popup: popups.append(popup))
            download_future = asyncio.create_task(page.wait_for_event("download", timeout=ctx["timeout"] * 1000))
            await button.click(timeout=ctx["timeout"] * 1000)
            download = None
            try:
                download = await download_future
            except PlaywrightTimeoutError:
                pass
            except Exception:
                pass
            if download:
                target = ctx["evidence_dir"] / f"iess-document-2-{time.time_ns()}.pdf"
                await download.save_as(target)
                if valid_pdf_for_ords(target):
                    return result("MATCH", None, target)
                target.unlink(missing_ok=True)

            # Some IESS deployments render the native PDF in a popup instead of downloading it.
            if popups:
                popup = popups[0]
                try:
                    await popup.wait_for_load_state("domcontentloaded", timeout=ctx["timeout"] * 1000)
                    pdf_url = popup.url
                    if pdf_url.lower().endswith(".pdf"):
                        pdf_response = await popup.request.get(pdf_url, timeout=ctx["timeout"] * 1000)
                        body = await pdf_response.body()
                        if pdf_response.status == 200:
                            target = ctx["evidence_dir"] / f"iess-document-2-{time.time_ns()}.pdf"
                            target.write_bytes(body)
                            if valid_pdf_for_ords(target):
                                return result("MATCH", None, target)
                            target.unlink(missing_ok=True)
                except Exception:
                    pass

            text = (await page.locator("body").inner_text()).casefold()
            if re.search(r"no se (?:encontró|encuentra)|no existe información|no registra obligaciones", text):
                target = ctx["evidence_dir"] / f"iess-document-2-{time.time_ns()}.png"
                await page.screenshot(path=str(target), full_page=True)
                return result("NO_MATCH", None, target)
            if challenge.search(text):
                return result("HUMAN_REQUIRED", "PORTAL_CHALLENGE")
            return result("RETRYABLE", "NATIVE_PDF_NOT_ACQUIRED")
        finally:
            await browser.close()


async def run(ctx: dict) -> dict:
    """Convertir errores tardíos de red/navegador en resultado recuperable."""
    try:
        return await _run(ctx)
    except PlaywrightTimeoutError:
        return result("RETRYABLE", "PORTAL_TIMEOUT")
    except Exception:
        return result("RETRYABLE", "PORTAL_OR_BROWSER_ERROR")


def result(status: str, reason: str | None, artifact: Path | None = None) -> dict:
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest() if artifact and artifact.exists() else None
    artifact_type = "PDF" if artifact and artifact.suffix.lower() == ".pdf" else "PNG" if artifact else None
    return {"adapter_id": ADAPTER_ID, "adapter_version": ADAPTER_VERSION,
            "document_id": 2, "status": status, "reason_code": reason,
            "artifact_type": artifact_type, "artifact_sha256": digest}


async def documento_2(work, services):
    """Generic motor ABI; portal controls remain isolated in this application."""
    if work.portal_id != 2 or work.document_id != 2:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    browser = services["browser"]
    target = Path(services["evidence_root"]) / f"iess-{work.detail_id}.pdf"
    try:
        await browser.goto(work.entry_url)
        if await browser.is_visible('iframe[src*="captcha"], [class*="altcha"]'):
            return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
        await browser.fill_role("textbox", "Cédula / RUC", work.subject.identification)
        # Match the historic PDF acquisition workflow through the installed
        # facade's download event. Do not submit the form a second time as a
        # speculative fallback after a timeout.
        await browser.download_by_click('button:has-text("CONSULTAR")', str(target))
        if not valid_pdf_for_ords(target):
            target.unlink(missing_ok=True)
            return {"kind": "RETRYABLE", "reason_code": "NATIVE_PDF_STRUCTURE_INVALID"}
        return {"kind": "MATCH", "evidence_path": str(target)}
    except Exception:
        target.unlink(missing_ok=True)
        return {"kind": "RETRYABLE", "reason_code": "NATIVE_PDF_NOT_ACQUIRED"}


DOCUMENT_FUNCTIONS = {"documento_2": documento_2}


def main() -> int:
    parser = argparse.ArgumentParser(description="IESS standalone TEST adapter")
    parser.add_argument("--context", required=True, type=Path)
    args = parser.parse_args()
    try:
        output = asyncio.run(run(load_context(args.context.resolve())))
    except Exception as exc:
        output = result("ERROR", "INVALID_CONTEXT_OR_RUNTIME")
        output["exception_type"] = type(exc).__name__
    print(json.dumps(output, separators=(",", ":")))
    return 0 if output["status"] in {"MATCH", "NO_MATCH"} else 1


if __name__ == "__main__":
    sys.exit(main())

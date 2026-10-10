"""Aplicación independiente OFAC para el documento de búsqueda 5."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

ADAPTER_ID = "ofac"
ADAPTER_VERSION = "0.1.4-candidate"
OFAC_HOST = "sanctionssearch.ofac.treas.gov"
RESULT_COUNT = re.compile(r"Lookup Results:\s*(\d+)\s*Found", re.I)
CHALLENGE = re.compile(r"captcha|altcha|verify you are human|no soy un robot", re.I)
PORTAL_BUSY = re.compile(r"please wait|searching|loading|espere por favor|\bcargando\b", re.I)
RESULT_STABLE_SAMPLES = 2
NAVIGATION_TIMEOUT_SECONDS = 30
ELEMENT_TIMEOUT_SECONDS = 15
RESULT_INITIAL_SECONDS = 45
RESULT_EXTENSION_SECONDS = 15
RESULT_MAX_SECONDS = 120
_human_barrier = False


def load_context(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("portal_id") != 5 or raw.get("document_id") != 5:
        raise ValueError("documento no soportado")
    url = urlparse(str(raw["entry_url"]))
    if url.scheme != "https" or url.hostname != OFAC_HOST:
        raise ValueError("URL de entrada no autorizada")
    if not str(raw.get("identification", "")).strip() or not str(raw.get("display_name", "")).strip():
        raise ValueError("contexto incompleto")
    repo = Path(__file__).resolve().parents[2]
    evidence_dir = Path(raw["evidence_dir"]).resolve()
    if path.resolve().is_relative_to(repo) or evidence_dir.is_relative_to(repo):
        raise ValueError("contexto y evidencia deben quedar fuera del repositorio")
    return {"url": str(raw["entry_url"]), "name": str(raw["display_name"]).strip(),
            "evidence_dir": evidence_dir,
            "timeout": min(RESULT_MAX_SECONDS,
                           max(RESULT_INITIAL_SECONDS,
                               int(raw.get("timeout_seconds", RESULT_MAX_SECONDS)))),
            "pacing": max(5.0, float(raw.get("pacing_seconds", 5)))}


def output(status: str, reason: str | None = None, evidence: Path | None = None) -> dict:
    digest = hashlib.sha256(evidence.read_bytes()).hexdigest() if evidence and evidence.exists() else None
    return {"adapter_id": ADAPTER_ID, "adapter_version": ADAPTER_VERSION,
            "document_id": 5, "status": status, "reason_code": reason,
            "evidence_type": "PNG" if evidence else None, "evidence_sha256": digest}


def _navigation_failure(exc: Exception) -> str:
    """Classify network failures without returning exception text or URLs."""
    if isinstance(exc, PlaywrightTimeoutError):
        return "PORTAL_NAVIGATION_TIMEOUT"
    message = str(exc).upper()
    markers = (
        ("ERR_INTERNET_DISCONNECTED", "NETWORK_DISCONNECTED"),
        ("ERR_NETWORK_CHANGED", "NETWORK_CHANGED"),
        ("ERR_CONNECTION_RESET", "PORTAL_CONNECTION_RESET"),
        ("ERR_CONNECTION_REFUSED", "PORTAL_CONNECTION_REFUSED"),
        ("ERR_NAME_NOT_RESOLVED", "PORTAL_DNS_FAILURE"),
        ("ERR_CONNECTION_TIMED_OUT", "PORTAL_CONNECTION_TIMEOUT"),
        ("ERR_TIMED_OUT", "PORTAL_CONNECTION_TIMEOUT"),
        ("ERR_ADDRESS_UNREACHABLE", "PORTAL_UNREACHABLE"),
    )
    return next((reason for marker, reason in markers if marker in message),
                "PORTAL_NAVIGATION_ERROR")


async def _run_on_page(ctx: dict, page) -> dict:
    ctx["evidence_dir"].mkdir(parents=True, exist_ok=True)
    try:
        response = await page.goto(ctx["url"], wait_until="domcontentloaded",
                                   timeout=NAVIGATION_TIMEOUT_SECONDS * 1000)
    except Exception as exc:
        return output("RETRYABLE", _navigation_failure(exc))
    if response and response.status in (403, 429, 451):
        return output("BLOCKED", f"HTTP_{response.status}")
    if CHALLENGE.search(await page.locator("body").inner_text()):
        return output("HUMAN_REQUIRED", "PORTAL_CHALLENGE")
    field = page.get_by_role("textbox", name="Enter name as search criteria.", exact=True)
    button = page.get_by_role("button", name="Search", exact=True)
    if await field.count() != 1 or await button.count() != 1:
        return output("RETRYABLE", "SEARCH_CONTROLS_NOT_UNIQUE")
    await page.wait_for_timeout(round(ctx["pacing"] * 1000))
    await field.fill(ctx["name"], timeout=ELEMENT_TIMEOUT_SECONDS * 1000)
    await page.wait_for_timeout(round(ctx["pacing"] * 1000))
    await button.click(timeout=ELEMENT_TIMEOUT_SECONDS * 1000)
    started = time.monotonic()
    absolute_deadline = started + min(ctx["timeout"], RESULT_MAX_SECONDS)
    deadline = min(absolute_deadline, started + RESULT_INITIAL_SECONDS)
    count = None
    stable_count = None
    stable_samples = 0
    while time.monotonic() < deadline:
        text = await page.locator("body").inner_text()
        if CHALLENGE.search(text):
            return output("HUMAN_REQUIRED", "PORTAL_CHALLENGE")
        busy = bool(PORTAL_BUSY.search(text))
        if busy:
            stable_count = None
            stable_samples = 0
            # An explicit portal loading state is progress; extend in bounded
            # increments, never beyond the absolute per-query deadline.
            deadline = min(absolute_deadline,
                           max(deadline, time.monotonic() + RESULT_EXTENSION_SECONDS))
            await page.wait_for_timeout(500)
            continue
        match = RESULT_COUNT.search(text)
        if match:
            observed = int(match.group(1))
            if observed == stable_count:
                stable_samples += 1
            else:
                stable_count = observed
                stable_samples = 1
                deadline = min(absolute_deadline,
                               max(deadline, time.monotonic() + RESULT_EXTENSION_SECONDS))
            if stable_samples >= RESULT_STABLE_SAMPLES:
                count = observed
                break
        else:
            stable_count = None
            stable_samples = 0
        await page.wait_for_timeout(500)
    if count is None:
        return output("RETRYABLE", "RESULT_COUNT_NOT_CONCLUSIVE")
    evidence = ctx["evidence_dir"] / f"ofac-document-5-{time.time_ns()}.png"
    await page.screenshot(path=str(evidence), full_page=True)
    return output("MATCH" if count else "NO_MATCH", evidence=evidence)


async def run_many(contexts: list[dict], *, headless: bool = True, on_result=None) -> list[dict]:
    """Run all ORDS-ordered work in one browser session and preserve cookies."""
    if not contexts:
        return []
    async with async_playwright() as p:
        browser = None
        for channel in ("msedge", "chrome"):
            try:
                browser = await p.chromium.launch(channel=channel, headless=headless)
                break
            except Exception:
                continue
        if browser is None:
            return [output("ERROR", "NO_SUPPORTED_BROWSER") for _ in contexts]
        page = await browser.new_page()
        try:
            results = []
            for ctx in contexts:
                try:
                    result = await _run_on_page(ctx, page)
                except Exception:
                    result = output("RETRYABLE", "PORTAL_ACTION_FAILED")
                results.append(result)
                if on_result is not None:
                    reported = on_result(len(results), result)
                    if asyncio.iscoroutine(reported):
                        await reported
                # Per-subject network/runtime failures are recorded and the
                # queue advances. Only explicit portal/legal barriers stop this
                # portal batch; the caller can then continue with another portal.
                if result["status"] in {"BLOCKED", "HUMAN_REQUIRED"}:
                    break
            return results
        finally:
            await browser.close()


async def prepare(_work, _services):
    """Clear the challenge latch once at the beginning of a sidecar batch."""
    global _human_barrier
    _human_barrier = False


async def run(ctx: dict) -> dict:
    return (await run_many([ctx]))[0]


async def documento_5(work, services):
    """CNTR RPA 1.0.0 sidecar ABI for the OFAC document 5."""
    global _human_barrier
    if work.portal_id != 5 or work.document_id != 5:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    if _human_barrier:
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE",
                "reason_code": "PORTAL_CHALLENGE"}
    browser = services["browser"]
    evidence = Path(services["evidence_root"]) / f"ofac-{work.detail_id}.png"
    try:
        await browser.goto(work.entry_url)
        challenge = 'iframe[src*="captcha"], [class*="altcha"]'
        if await browser.is_visible(challenge):
            _human_barrier = True
            return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
        await browser.fill_role("textbox", "Enter name as search criteria.",
                                work.subject.display_name, exact=True)
        await browser.click_role("button", "Search", exact=True)
        deadline = time.monotonic() + min(work.deadline_seconds, 120)
        stable_count = None
        stable_samples = 0
        while time.monotonic() < deadline:
            if await browser.is_visible(challenge):
                _human_barrier = True
                return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
            text = await browser.text("body")
            if PORTAL_BUSY.search(text):
                stable_count = None
                stable_samples = 0
                await asyncio.sleep(0.5)
                continue
            match = RESULT_COUNT.search(text)
            if match:
                observed = int(match.group(1))
                if observed == stable_count:
                    stable_samples += 1
                else:
                    stable_count = observed
                    stable_samples = 1
                if stable_samples >= RESULT_STABLE_SAMPLES:
                    await browser.screenshot(str(evidence), full_page=True)
                    return {"kind": "MATCH" if observed else "NO_MATCH",
                            "evidence_path": str(evidence)}
            else:
                stable_count = None
                stable_samples = 0
            await asyncio.sleep(0.5)
        return {"kind": "RETRYABLE", "reason_code": "RESULT_COUNT_NOT_CONCLUSIVE"}
    except Exception:
        evidence.unlink(missing_ok=True)
        return {"kind": "RETRYABLE", "reason_code": "OFAC_SEARCH_FAILED"}


DOCUMENT_FUNCTIONS = {"documento_5": documento_5}


def main() -> int:
    parser = argparse.ArgumentParser(description="OFAC standalone TEST adapter")
    parser.add_argument("--context", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = asyncio.run(run(load_context(args.context.resolve())))
    except Exception as exc:
        result = output("ERROR", "INVALID_CONTEXT_OR_RUNTIME")
        result["exception_type"] = type(exc).__name__
    print(json.dumps(result, separators=(",", ":")))
    return 0 if result["status"] in {"MATCH", "NO_MATCH"} else 1


if __name__ == "__main__":
    sys.exit(main())

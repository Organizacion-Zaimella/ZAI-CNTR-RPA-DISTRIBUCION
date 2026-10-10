"""Aplicación standalone TEST para el adaptador del Consejo de la Judicatura.

La entrada contiene únicamente el plan autorizado local; no llama ORDS ni
incluye identidades en stdout. Ejecuta los trabajos en el orden recibido y
conserva una página Playwright durante todo el lote.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace

from playwright.async_api import async_playwright


APP_DIR = Path(__file__).resolve().parent
ADAPTER_PATH = APP_DIR / "src" / "adapter.py"
SPEC = importlib.util.spec_from_file_location("judicatura_standalone_adapter", ADAPTER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("adaptador no disponible")
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


def load_context(path: Path) -> tuple[list[SimpleNamespace], Path]:
    source = path.resolve(strict=True)
    if source.is_relative_to(APP_DIR.parent.parent):
        raise ValueError("contexto dentro del repositorio")
    raw = json.loads(source.read_text(encoding="utf-8"))
    if raw.get("portal_id") != 6 or not isinstance(raw.get("works"), list):
        raise ValueError("contexto no soportado")
    evidence_root = Path(raw["evidence_dir"]).resolve()
    if evidence_root.is_relative_to(APP_DIR.parent.parent):
        raise ValueError("evidencia dentro del repositorio")
    evidence_root.mkdir(parents=True, exist_ok=True)
    if not 1 <= len(raw["works"]) <= 20:
        raise ValueError("lote fuera de límites")
    standalone_mode = raw.get("standalone_mode") is True
    works = []
    for ordinal, item in enumerate(raw["works"], start=1):
        if type(item.get("document_id")) is not int or item["document_id"] not in adapter.FIELDS:
            raise ValueError("documento no soportado")
        subject = item.get("subject")
        if not isinstance(subject, dict):
            raise ValueError("sujeto ausente")
        if any(not isinstance(subject.get(field), str) or not subject[field].strip()
               for field in ("identification", "display_name")):
            raise ValueError("datos de consulta incompletos")
        if standalone_mode and "execution_id" not in item and "detail_id" not in item:
            # Local-only filenames; these values are never sent to ORDS and
            # must not be mistaken for CNTR execution/detail identifiers.
            execution_id, detail_id = "standalone", f"{item['document_id']}-{ordinal:03d}"
        else:
            try:
                execution_id, detail_id = int(item["execution_id"]), int(item["detail_id"])
            except (KeyError, TypeError, ValueError):
                raise ValueError("correlación inválida") from None
        work = SimpleNamespace(
            portal_id=6,
            document_id=item["document_id"],
            entry_url=adapter._safe_entry(item["entry_url"]),
            execution_id=execution_id,
            detail_id=detail_id,
            deadline_seconds=min(3600, max(1, int(item.get("deadline_seconds", 300)))),
            subject=SimpleNamespace(
                id=int(subject.get("id", 0)),
                type=subject.get("type", "PERSONA"),
                origin=subject.get("origin", "NACIONAL"),
                identification=subject["identification"],
                display_name=subject["display_name"],
                names=subject.get("names"),
                surnames=subject.get("surnames"),
            ),
        )
        if not standalone_mode or "execution_id" in item or "detail_id" in item:
            if not isinstance(work.execution_id, int) or not isinstance(work.detail_id, int) or work.execution_id <= 0 or work.detail_id <= 0:
                raise ValueError("correlación inválida")
        works.append(work)
    return works, evidence_root


class Pacer:
    def __init__(self, interval: float = 5.0):
        self.interval = interval
        self.last_action: float | None = None

    async def act(self, operation):
        now = time.monotonic()
        if self.last_action is not None:
            delay = self.interval - (now - self.last_action)
            if delay > 0:
                await asyncio.sleep(delay)
        self.last_action = time.monotonic()
        return await operation()


class BrowserFacade:
    """Subset of PortalActions needed by the Judicatura adapter."""
    def __init__(self, page):
        self.page = page
        self.pacer = Pacer()

    def locator(self, selector: str):
        return self.page.locator(selector)

    async def goto(self, url: str, **kwargs):
        return await self.pacer.act(lambda: self.page.goto(
            url, wait_until="domcontentloaded", **kwargs))

    async def wait_for_selector(self, selector: str, **kwargs):
        return await self.locator(selector).wait_for(**kwargs)

    async def fill(self, selector: str, value: str):
        return await self.pacer.act(lambda: self.locator(selector).fill(value))

    async def input_value(self, selector: str):
        return await self.locator(selector).input_value()

    async def click(self, selector: str):
        return await self.pacer.act(lambda: self.locator(selector).click())

    async def is_visible(self, selector: str):
        return await self.locator(selector).is_visible()

    async def count(self, selector: str):
        return await self.locator(selector).count()

    async def text(self, selector: str):
        return await self.locator(selector).inner_text()

    async def search_idle(self):
        return bool(await self.page.evaluate("""() => {
            const queue = window.PrimeFaces?.ajax?.Queue;
            return Boolean(queue && queue.isEmpty());
        }"""))

    async def progress_token(self):
        """Return a low-sensitivity signal for ongoing navigation/result loading."""
        return await self.page.evaluate("""() => {
            const entries = performance.getEntriesByType('resource');
            return JSON.stringify({
                url: location.href,
                textLength: document.body?.innerText?.length || 0,
                rows: document.querySelectorAll('table tr').length,
                resources: entries.length,
                transfer: entries.reduce((sum, item) => sum + (item.transferSize || 0), 0)
            });
        }""")

    async def screenshot(self, path: str, *, full_page: bool = True):
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        return await self.page.screenshot(path=str(target), full_page=full_page)


async def run_context(works: list[SimpleNamespace], evidence_root: Path,
                      *, headless: bool = True) -> list[dict]:
    async with async_playwright() as playwright:
        browser = None
        for channel in ("msedge", "chrome"):
            try:
                browser = await playwright.chromium.launch(channel=channel, headless=headless)
                break
            except Exception:
                continue
        if browser is None:
            return [{"document_id": w.document_id, "status": "ERROR",
                     "reason_code": "NO_SUPPORTED_BROWSER"} for w in works]
        try:
            page = await browser.new_page()
            services = {"browser": BrowserFacade(page), "evidence_root": evidence_root}
            await adapter.prepare(works[0], services)
            results = []
            for work in works:  # ORDS order is preserved; no sorting or regrouping.
                try:
                    result = await adapter.execute_document(work, services)
                except Exception:
                    result = {"kind": "RETRYABLE", "reason_code": "PORTAL_INTERACTION_FAILED"}
                item = {"document_id": work.document_id, "status": result["kind"],
                        "reason_code": result.get("reason_code"),
                        "recovery_click_used": result.get("recovery_click_used", False)}
                evidence = result.get("evidence_path")
                if evidence:
                    payload = Path(evidence).read_bytes()
                    item["evidence_sha256"] = hashlib.sha256(payload).hexdigest()
                results.append(item)
            return results
        finally:
            await browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Consejo de la Judicatura standalone TEST")
    parser.add_argument("--context", required=True, type=Path)
    parser.add_argument("--headed", action="store_true")
    args = parser.parse_args()
    try:
        works, evidence_root = load_context(args.context)
        results = asyncio.run(run_context(works, evidence_root, headless=not args.headed))
        print(json.dumps({"portal_id": 6, "results": results}, separators=(",", ":")))
        return 0 if all(item["status"] in {"MATCH", "NO_MATCH", "HUMAN_REQUIRED", "RETRYABLE"}
                        for item in results) else 1
    except Exception:
        print(json.dumps({"portal_id": 6, "status": "ERROR",
                          "reason_code": "INVALID_CONTEXT_OR_RUNTIME"}, separators=(",", ":")))
        return 2


if __name__ == "__main__":
    sys.exit(main())

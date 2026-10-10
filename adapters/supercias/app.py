"""Aplicación standalone TEST de Superintendencia, documentos 13–19."""
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
from urllib.parse import urljoin, urlsplit

from playwright.async_api import async_playwright


APP_DIR = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("supercias_standalone_adapter", APP_DIR / "adapter.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("adaptador no disponible")
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)
MAX_PDF_BYTES = 50 * 1024 * 1024


def _private_path(raw: str, *, must_exist: bool) -> Path:
    path = Path(raw).resolve(strict=must_exist)
    if path.is_relative_to(APP_DIR.parent.parent):
        raise ValueError("ruta privada dentro del repositorio")
    return path


def load_context(path: Path) -> tuple[list[SimpleNamespace], Path]:
    source = path.resolve(strict=True)
    if source.is_relative_to(APP_DIR.parent.parent):
        raise ValueError("contexto dentro del repositorio")
    raw = json.loads(source.read_text(encoding="utf-8"))
    if raw.get("portal_id") != 1 or not isinstance(raw.get("works"), list):
        raise ValueError("contexto no soportado")
    evidence_root = _private_path(raw.get("evidence_dir", ""), must_exist=False)
    evidence_root.mkdir(parents=True, exist_ok=True)
    if not 1 <= len(raw["works"]) <= 20:
        raise ValueError("lote fuera de límites")
    works = []
    subject_key = None
    for item in raw["works"]:
        if not isinstance(item, dict) or type(item.get("document_id")) is not int:
            raise ValueError("documento inválido")
        document_id = item["document_id"]
        if document_id not in adapter.DOCUMENTS:
            raise ValueError("documento no soportado")
        subject = item.get("subject")
        if not isinstance(subject, dict) or subject.get("type") != "EMPRESA":
            raise ValueError("solo admite sujetos empresa")
        for field in ("identification", "display_name"):
            if not isinstance(subject.get(field), str) or not subject[field].strip():
                raise ValueError("datos de consulta incompletos")
        entry = urlsplit(str(item.get("entry_url", "")))
        if (entry.scheme != "https" or entry.hostname != adapter.EXPECTED_HOST
                or entry.username or entry.password or entry.fragment):
            raise ValueError("origen no autorizado")
        identity = (subject.get("id"), subject["identification"], subject["display_name"])
        if subject_key is None:
            subject_key = identity
        elif subject_key != identity:
            raise ValueError("un lote debe pertenecer a un solo sujeto")
        execution_id, detail_id = int(item["execution_id"]), int(item["detail_id"])
        if execution_id <= 0 or detail_id <= 0:
            raise ValueError("correlación inválida")
        work = SimpleNamespace(
            portal_id=1, document_id=document_id,
            entry_url=item["entry_url"],
            execution_id=execution_id, detail_id=detail_id,
            deadline_seconds=min(3600, max(1, int(item.get("deadline_seconds", 300)))),
            subject=SimpleNamespace(
                id=int(subject.get("id", 0)),
                type=SimpleNamespace(value="EMPRESA"),
                identification=subject["identification"].strip(),
                display_name=subject["display_name"].strip(),
            ),
        )
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
    """Standalone equivalent of the generic PortalActions browser surface."""
    def __init__(self, page):
        self.page = page
        self.pacer = Pacer()

    def _loc(self, selector: str):
        return self.page.locator(selector)

    async def goto(self, url: str, **kwargs):
        return await self.pacer.act(lambda: self.page.goto(
            url, wait_until="domcontentloaded", **kwargs))

    async def count(self, selector: str):
        return await self._loc(selector).count()

    async def is_visible(self, selector: str):
        return await self._loc(selector).is_visible()

    async def is_checked(self, selector: str):
        return await self._loc(selector).is_checked()

    async def text(self, selector: str):
        return await self._loc(selector).inner_text()

    async def attribute(self, selector: str, name: str):
        return await self._loc(selector).get_attribute(name)

    async def fill(self, selector: str, value: str):
        return await self.pacer.act(lambda: self._loc(selector).fill(value))

    async def press(self, selector: str, key: str):
        return await self.pacer.act(lambda: self._loc(selector).press(key))

    async def type_text(self, selector: str, value: str):
        locator = self._loc(selector)
        for character in value:
            await self.pacer.act(lambda character=character: locator.press(character))
            barrier = 'altcha-widget:not([state="verified"])'
            count = await self.count(barrier)
            if count > 1 or (count == 1 and await self.is_visible(barrier)):
                raise adapter.HumanBarrier("ruc_keyboard")

    async def click(self, selector: str):
        return await self.pacer.act(lambda: self._loc(selector).click())

    async def click_role(self, role: str, name: str):
        locator = self.page.get_by_role(role, name=name)
        return await self.pacer.act(locator.click)

    async def wait_for_selector(self, selector: str, **kwargs):
        return await self._loc(selector).wait_for(**kwargs)

    async def screenshot(self, path: str, *, full_page: bool = True):
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        return await self.page.screenshot(path=str(target), full_page=full_page)

    async def save_same_origin_pdf_from_dialog(self, dialog_selector: str, destination: str):
        nodes = self._loc(dialog_selector).locator("object[data],embed[src],iframe[src]")
        if await nodes.count() != 1:
            raise ValueError("visor PDF ambiguo")
        node = nodes.first
        candidate = await node.get_attribute("data") or await node.get_attribute("src")
        if not candidate:
            raise ValueError("visor PDF sin origen")
        target_url = urljoin(self.page.url, candidate)
        current, target = urlsplit(self.page.url), urlsplit(target_url)
        if ((target.scheme, target.netloc) != (current.scheme, current.netloc)
                or target.username or target.password):
            raise ValueError("PDF fuera de origen")
        response = await self.pacer.act(lambda: self.page.context.request.get(
            target_url, max_redirects=0, timeout=30000))
        mime = response.headers.get("content-type", "").lower()
        if response.status != 200 or "application/pdf" not in mime:
            raise ValueError("respuesta PDF inválida")
        body = await response.body()
        if (not body.startswith(b"%PDF-") or b"%%EOF" not in body[-2048:]
                or len(body) > MAX_PDF_BYTES):
            raise ValueError("bytes PDF inválidos")
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        return path


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
            for work in works:  # Respetar el orden del plan recibido.
                try:
                    result = await adapter.execute_document(work, services)
                except Exception:
                    result = {"kind": "RETRYABLE", "reason_code": "PORTAL_ADAPTER_FAILURE"}
                item = {"document_id": work.document_id, "status": result["kind"],
                        "reason_code": result.get("reason_code")}
                evidence_path = result.get("evidence_path")
                if evidence_path:
                    item["evidence_sha256"] = hashlib.sha256(
                        Path(evidence_path).read_bytes()).hexdigest()
                results.append(item)
            return results
        finally:
            await browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Superintendencia standalone TEST")
    parser.add_argument("--context", required=True, type=Path)
    parser.add_argument("--headed", action="store_true")
    args = parser.parse_args()
    try:
        works, evidence_root = load_context(args.context)
        results = asyncio.run(run_context(works, evidence_root, headless=not args.headed))
        print(json.dumps({"portal_id": 1, "results": results}, separators=(",", ":")))
        return 0 if all(item["status"] in {"MATCH", "HUMAN_REQUIRED", "RETRYABLE"}
                        for item in results) else 1
    except Exception:
        print(json.dumps({"portal_id": 1, "status": "ERROR",
                          "reason_code": "INVALID_CONTEXT_OR_RUNTIME"}, separators=(",", ":")))
        return 2


if __name__ == "__main__":
    sys.exit(main())

"""Pruebas del runner standalone sin portal ni ORDS."""
from __future__ import annotations

import asyncio
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
SPEC = importlib.util.spec_from_file_location("supercias_standalone_app_test", APP_PATH)
app = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(app)


class Browser:
    def __init__(self):
        self.pages = []
        self.close_calls = 0

    async def new_page(self):
        page = object()
        self.pages.append(page)
        return page

    async def close(self):
        self.close_calls += 1


class Playwright:
    def __init__(self):
        self.browser = Browser()
        self.chromium = SimpleNamespace(launch=self.launch)

    async def launch(self, **_kwargs):
        return self.browser

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return None


class TypingLocator:
    def __init__(self, page, selector):
        self.page, self.selector = page, selector

    async def press(self, value):
        if self.selector == "company-field":
            self.page.typed.append(value)

    async def count(self):
        return int("altcha-widget" in self.selector and len(self.page.typed) >= 2)

    async def is_visible(self):
        return await self.count() == 1


class TypingPage:
    def __init__(self):
        self.typed = []

    def locator(self, selector):
        return TypingLocator(self, selector)


class PdfNode:
    def __init__(self, url):
        self.url = url

    async def get_attribute(self, name):
        return self.url if name == "data" else None


class PdfNodes:
    def __init__(self, url):
        self.first = PdfNode(url)

    async def count(self):
        return 1


class PdfContext:
    def __init__(self, response):
        self.request = self
        self.response = response
        self.calls = []

    async def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.response


class PdfPage:
    url = "https://appscvsgen.supercias.gob.ec/dialog"

    def __init__(self, candidate, response):
        self.candidate = candidate
        self.context = PdfContext(response)

    def locator(self, _selector):
        return SimpleNamespace(locator=lambda _nested: PdfNodes(self.candidate))


class PdfResponse:
    status = 200
    headers = {"content-type": "application/pdf"}

    def __init__(self, body):
        self.value = body

    async def body(self):
        return self.value


def test_context_rejects_person_or_unapproved_origin(tmp_path):
    context = tmp_path / "context.json"
    base = {"portal_id": 1, "evidence_dir": str(tmp_path / "evidence"), "works": [{
        "document_id": 13, "entry_url": "https://appscvsgen.supercias.gob.ec/consulta/",
        "execution_id": 1, "detail_id": 2,
        "subject": {"id": 1, "type": "EMPRESA", "identification": "test-id",
                    "display_name": "test entity"},
    }]}
    context.write_text(json.dumps(base), encoding="utf-8")
    works, _ = app.load_context(context)
    assert works[0].document_id == 13

    base["works"][0]["subject"]["type"] = "PERSONA"
    context.write_text(json.dumps(base), encoding="utf-8")
    try:
        app.load_context(context)
    except ValueError:
        pass
    else:
        raise AssertionError("PERSONA debe rechazarse")


def test_runner_continues_in_same_browser_after_one_work_failure(tmp_path, monkeypatch):
    playwright = Playwright()
    monkeypatch.setattr(app, "async_playwright", lambda: playwright)
    seen = []

    async def prepare(_work, _services):
        return None

    async def execute(work, services):
        seen.append((work.document_id, id(services["browser"].page)))
        if work.document_id == 13:
            raise TimeoutError("private provider detail")
        return {"kind": "HUMAN_REQUIRED", "reason_code": "PORTAL_CHALLENGE"}

    monkeypatch.setattr(app.adapter, "prepare", prepare)
    monkeypatch.setattr(app.adapter, "execute_document", execute)
    works = [SimpleNamespace(document_id=13), SimpleNamespace(document_id=14)]

    results = asyncio.run(app.run_context(works, tmp_path))

    assert [item["status"] for item in results] == ["RETRYABLE", "HUMAN_REQUIRED"]
    assert [item[0] for item in seen] == [13, 14]
    assert seen[0][1] == seen[1][1]
    assert len(playwright.browser.pages) == 1
    assert playwright.browser.close_calls == 1


def test_pdf_capture_requires_same_origin_and_valid_pdf_bytes(tmp_path):
    async def scenario():
        body = b"%PDF-1.7\nexample\n%%EOF"
        page = PdfPage("/content/document.pdf", PdfResponse(body))
        result = await app.BrowserFacade(page).save_same_origin_pdf_from_dialog(
            ".ui-dialog", str(tmp_path / "result.pdf"))
        assert result.read_bytes() == body
        assert page.context.calls[0][1]["max_redirects"] == 0

        external = PdfPage("https://example.invalid/document.pdf", PdfResponse(body))
        try:
            await app.BrowserFacade(external).save_same_origin_pdf_from_dialog(
                ".ui-dialog", str(tmp_path / "should-not-exist.pdf"))
        except ValueError:
            pass
        else:
            raise AssertionError("debe rechazarse origen externo")
        assert external.context.calls == []

    asyncio.run(scenario())


def test_standalone_typing_stops_immediately_when_altcha_appears():
    async def scenario():
        page = TypingPage()
        browser = app.BrowserFacade(page)
        browser.pacer.interval = 0
        try:
            await browser.type_text("company-field", "12345")
        except app.adapter.HumanBarrier as barrier:
            assert barrier.phase == "ruc_keyboard"
        else:
            raise AssertionError("ALTCHA debe interrumpir el tecleo")
        assert len(page.typed) == 2

    asyncio.run(scenario())

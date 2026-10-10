"""Pruebas locales del tratamiento de fallos, sin abrir el portal SRI."""
from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
SPEC = importlib.util.spec_from_file_location("sri_standalone_app", APP_PATH)
app = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = app
SPEC.loader.exec_module(app)


def context():
    return app.WorkContext(document_id=53,
                           entry_url="https://srienlinea.sri.gob.ec/sri-en-linea/SriRucWeb/ConsultaRuc/Consultas/consultaRuc",
                           identification="TEST-ONLY", evidence_dir=Path("."))


class SidecarBrowser:
    def __init__(self):
        self.challenge = False
        self.actions = []

    async def goto(self, url):
        self.actions.append("goto")

    async def is_visible(self, selector):
        return self.challenge

    async def fill_role(self, *args, **kwargs):
        self.actions.append("fill")

    async def type_text(self, *args, **kwargs):
        self.actions.append("type")

    async def enabled(self, selector):
        return True

    async def click_role(self, *args, **kwargs):
        self.actions.append("click")
        self.challenge = True


def work(document_id, detail_id):
    return SimpleNamespace(
        portal_id=3, document_id=document_id, detail_id=detail_id,
        entry_url="https://srienlinea.sri.gob.ec" + app.DOCUMENT_ROUTES[document_id],
        deadline_seconds=10,
        subject=SimpleNamespace(identification="TEST-ONLY"),
    )


def run(coro):
    return asyncio.run(coro)


def test_late_playwright_timeout_is_retryable_without_exception_text():
    async def timeout(_context):
        raise app.PlaywrightTimeoutError("private portal response")

    with patch.object(app, "_run", timeout):
        result = run(app.run(context()))

    assert result["status"] == "RETRYABLE"
    assert result["reason_code"] == "PORTAL_TIMEOUT"
    assert "private portal response" not in str(result)


def test_browser_error_is_retryable_without_exception_text():
    async def failure(_context):
        raise RuntimeError("private connection details")

    with patch.object(app, "_run", failure):
        result = run(app.run(context()))

    assert result["status"] == "RETRYABLE"
    assert result["reason_code"] == "PORTAL_OR_BROWSER_ERROR"
    assert "private connection details" not in str(result)


def test_connection_reset_is_sanitized_before_any_subject_input():
    class FailedNavigation:
        def __init__(self, error):
            self.error = error

        async def goto(self, _url, **_kwargs):
            raise self.error

    async def scenario():
        return await app._run_on_page(context(), FailedNavigation(
            RuntimeError("net::ERR_CONNECTION_RESET https://private.invalid/subject/123")))

    result = run(scenario())

    assert result["status"] == "RETRYABLE"
    assert result["reason_code"] == "PORTAL_CONNECTION_RESET"
    assert "private.invalid" not in str(result)
    assert "123" not in str(result)


def test_navigation_timeout_is_sanitized_without_retrying_the_portal():
    class FailedNavigation:
        calls = 0

        async def goto(self, _url, **_kwargs):
            self.calls += 1
            raise app.PlaywrightTimeoutError("private portal URL")

    page = FailedNavigation()
    result = run(app._run_on_page(context(), page))

    assert result["status"] == "RETRYABLE"
    assert result["reason_code"] == "PORTAL_NAVIGATION_TIMEOUT"
    assert page.calls == 1
    assert "private portal URL" not in str(result)


def test_internet_disconnect_is_classified_and_does_not_retry_navigation():
    class FailedNavigation:
        calls = 0

        async def goto(self, _url, **_kwargs):
            self.calls += 1
            raise RuntimeError("net::ERR_INTERNET_DISCONNECTED https://private.invalid/subject/123")

    page = FailedNavigation()
    result = run(app._run_on_page(context(), page))

    assert result["status"] == "RETRYABLE"
    assert result["reason_code"] == "NETWORK_DISCONNECTED"
    assert page.calls == 1
    assert "private.invalid" not in str(result)
    assert "123" not in str(result)


def test_sidecar_challenge_latch_skips_other_document_without_navigation():
    browser = SidecarBrowser()
    services = {"browser": browser, "evidence_root": Path(".")}

    async def scenario():
        await app.prepare(work(3, 1), services)
        first = await app.documento_3(work(3, 1), services)
        second = await app.documento_53(work(53, 2), services)
        return first, second

    first, second = run(scenario())

    assert first["kind"] == "HUMAN_REQUIRED"
    assert second["kind"] == "HUMAN_REQUIRED"
    assert browser.actions == ["goto", "fill", "type", "click"]


def test_run_many_keeps_browser_session_and_advances_after_network_loss():
    contexts = [context(), app.WorkContext(
        document_id=3, entry_url="https://example.invalid/next",
        identification="TEST-ONLY", evidence_dir=Path("."))]
    browser = SimpleNamespace(new_page=AsyncMock(return_value=object()), close=AsyncMock())
    playwright = SimpleNamespace()
    manager = AsyncMock()
    manager.__aenter__ = AsyncMock(return_value=playwright)
    manager.__aexit__ = AsyncMock(return_value=None)
    calls = []

    async def run_item(item, _page):
        calls.append(item.document_id)
        if len(calls) == 1:
            return app._result(item, "RETRYABLE", "PORTAL_CONNECTION_RESET")
        return app._result(item, "NO_MATCH")

    async def launch(_playwright, _headless):
        return browser

    with patch.object(app, "async_playwright", return_value=manager), \
         patch.object(app, "_launch_browser", launch), \
         patch.object(app, "_run_on_page", run_item):
        results = run(app.run_many(contexts))

    assert [result["status"] for result in results] == ["RETRYABLE", "NO_MATCH"]
    assert calls == [53, 3]
    browser.new_page.assert_awaited_once()
    browser.close.assert_awaited_once()

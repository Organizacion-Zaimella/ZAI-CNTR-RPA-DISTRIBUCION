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
TEST_RUC = "1790000000001"


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


def test_positive_classification_requires_the_exact_queried_ruc():
    assert app._classify(
        3, f"RUC: 179-0000000001; AL DÍA EN SUS OBLIGACIONES", TEST_RUC) == "MATCH"
    assert app._classify(
        3, "AL DÍA EN SUS OBLIGACIONES", TEST_RUC) == "MATCH_NOT_ATTRIBUTED"
    static_intro = "Conozca si se encuentra al día en sus obligaciones tributarias"
    assert app._classify(3, static_intro, TEST_RUC, static_intro) is None
    assert app._classify(
        53, f"RUC: {TEST_RUC}; estado: ACTIVO", TEST_RUC) == "MATCH"


def test_wait_profile_uses_short_initial_window_and_progress_extensions():
    assert app.NAVIGATION_TIMEOUT_SECONDS == 30
    assert app.ELEMENT_TIMEOUT_SECONDS == 15
    assert app.RESULT_INITIAL_SECONDS == 45
    assert app.RESULT_EXTENSION_SECONDS == 15
    assert app.RESULT_TIMEOUT_SECONDS == 120
    assert app.RESULT_BUSY.search("cargando información")
    assert app.RESULT_BUSY.search("procesando consulta")


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


def test_query_button_replacement_does_not_trigger_playwright_default_timeout():
    class Button:
        def __init__(self):
            self.enabled_checks = 0
            self.timeouts = []

        async def count(self):
            return 1

        async def is_visible(self, **_kwargs):
            return True

        async def is_enabled(self, *, timeout=None):
            self.timeouts.append(timeout)
            self.enabled_checks += 1
            if self.enabled_checks == 1:
                raise app.PlaywrightTimeoutError("detached during Angular update")
            return True

    class Page:
        def __init__(self):
            self.waits = []

        async def wait_for_timeout(self, duration):
            self.waits.append(duration)

    async def scenario():
        button, page = Button(), Page()
        enabled = await app._wait_query_button_enabled(page, button, 1)
        return enabled, button, page

    enabled, button, page = run(scenario())

    assert enabled is True
    assert button.enabled_checks == 2
    assert button.timeouts == [250, 250]
    assert page.waits == [250]


def test_query_button_absence_returns_within_operation_deadline():
    class Button:
        async def count(self):
            return 0

        async def is_visible(self, **_kwargs):
            raise AssertionError("hidden button must not be queried")

        async def is_enabled(self, **_kwargs):
            raise AssertionError("missing button must not wait implicitly")

    class Page:
        async def wait_for_timeout(self, duration):
            await asyncio.sleep(duration / 1000)

    enabled = run(app._wait_query_button_enabled(Page(), Button(), 0.02))

    assert enabled is False


def test_navigation_error_resumes_only_from_loaded_document_form_checkpoint(tmp_path):
    class Locator:
        def __init__(self, *, visible=False, text="", on_click=None):
            self.visible = visible
            self.text = text
            self.on_click = on_click

        async def count(self):
            return 1 if self.visible or self.text else 0

        async def is_visible(self):
            return self.visible

        async def wait_for(self, **_kwargs):
            pass

        async def fill(self, _value, **_kwargs):
            pass

        async def click(self, **_kwargs):
            if self.on_click:
                self.on_click()

        async def is_enabled(self, **_kwargs):
            return True

        async def inner_text(self):
            return self.text

        @property
        def first(self):
            return self

    class LoadedAfterErrorPage:
        url = context().entry_url

        def __init__(self):
            self.goto_calls = 0
            self.submitted = False
            self.keyboard = SimpleNamespace(type=AsyncMock())

        async def goto(self, *_args, **_kwargs):
            self.goto_calls += 1
            raise RuntimeError("net::ERR_CONNECTION_RESET")

        def locator(self, selector):
            if selector == "#busquedaRucId":
                return Locator(visible=True)
            if selector == "main":
                return Locator()
            if "captcha" in selector:
                return Locator()
            return Locator(text=("no se encontraron resultados" if self.submitted else "Consulta"))

        def get_by_role(self, _role, name, **_kwargs):
            return Locator(visible=name == "Consultar",
                           on_click=lambda: setattr(self, "submitted", True))

        async def wait_for_timeout(self, _duration):
            pass

        async def screenshot(self, *, path, **_kwargs):
            Path(path).write_bytes(b"synthetic screenshot")

    page = LoadedAfterErrorPage()
    ctx = app.WorkContext(context().document_id, context().entry_url,
                          context().identification, tmp_path)
    with patch.object(app, "ActionPacer", return_value=SimpleNamespace(
            before_action=AsyncMock(), mark=lambda: None)):
        result = run(app._run_on_page(ctx, page))

    assert result["status"] == "NO_MATCH"
    assert page.goto_calls == 1
    assert len(list(tmp_path.glob("sri-53-*.png"))) == 1


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


def test_optional_search_mode_click_obeys_the_five_second_action_pacer(tmp_path):
    class PacerSpy:
        def __init__(self, _interval):
            self.before_calls = 0

        async def before_action(self):
            self.before_calls += 1

        def mark(self):
            pass

    class Locator:
        def __init__(self, *, count=1, text="", on_click=None):
            self.count_value = count
            self.text = text
            self.on_click = on_click

        async def count(self):
            return self.count_value

        async def click(self, **_kwargs):
            if self.on_click:
                self.on_click()

        async def wait_for(self, **_kwargs):
            pass

        async def is_enabled(self, **_kwargs):
            return True

        async def fill(self, _value, **_kwargs):
            pass

        async def inner_text(self):
            return self.text

        @property
        def first(self):
            return self

    class Page:
        url = context().entry_url

        def __init__(self):
            self.keyboard = SimpleNamespace(type=AsyncMock())
            self.submitted = False
            self.mode = Locator()

        async def goto(self, *_args, **_kwargs):
            return None

        def locator(self, selector):
            if "captcha" in selector:
                return Locator(count=0)
            return Locator(text=("no se encontraron resultados" if self.submitted else "Consulta"))

        def get_by_role(self, _role, name, **_kwargs):
            if name.startswith("Seleccionar búsqueda"):
                return self.mode
            return Locator(on_click=lambda: setattr(self, "submitted", True))

        async def wait_for_timeout(self, _duration):
            pass

        async def screenshot(self, *, path, **_kwargs):
            Path(path).write_bytes(b"synthetic screenshot")

    pacer = PacerSpy(5)
    page = Page()
    ctx = app.WorkContext(context().document_id, context().entry_url,
                          context().identification, tmp_path)
    with patch.object(app, "ActionPacer", return_value=pacer):
        result = run(app._run_on_page(ctx, page))

    assert result["status"] == "NO_MATCH"
    # Search-mode click, field entry, and the one submit each have a paced wait.
    assert pacer.before_calls == 3


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

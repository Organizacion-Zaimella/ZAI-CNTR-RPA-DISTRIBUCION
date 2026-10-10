"""Regresión sintética del ABI SRI; no abre el portal ni usa datos reales."""
from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace


ADAPTER_PATH = Path(__file__).resolve().parents[1] / "src" / "adapter.py"
TEST_RUC = "1790000000001"
SPEC = importlib.util.spec_from_file_location("sri_sidecar_under_test", ADAPTER_PATH)
adapter = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = adapter
SPEC.loader.exec_module(adapter)


class Browser:
    def __init__(self):
        self.actions = []
        self.value = ""
        self.controls_ready = True
        self.result_text = "Formulario listo"
        self.query_result_text = "No se encontraron resultados"

    async def goto(self, url, **options):
        self.actions.append(("goto", url, options))

    async def goto_commit(self, url):
        self.actions.append(("goto_commit", url))

    async def is_visible(self, selector):
        return False

    async def count(self, selector):
        if not self.controls_ready:
            return 0
        if "Seleccionar búsqueda" in selector:
            return 1
        if selector == "#busquedaRucId":
            return 1
        return 0

    async def wait_for_selector(self, selector, **options):
        self.actions.append(("wait_for_selector", selector, options))
        self.controls_ready = True

    async def click_text(self, text, *, exact=False):
        self.actions.append(("mode", text, exact))

    async def fill(self, selector, value):
        self.actions.append(("fill", selector, value))
        self.value = value

    async def click(self, selector):
        self.actions.append(("click", selector))

    async def type_text(self, selector, value):
        self.actions.append(("type", selector))
        self.value = value

    async def input_value(self, selector):
        return self.value

    async def enabled(self, selector):
        return True

    async def click_role(self, role, name, *, exact=False):
        self.actions.append(("submit", role, name, exact))
        self.result_text = self.query_result_text

    async def text(self, selector):
        self.actions.append(("text", selector))
        return self.result_text

    async def screenshot(self, path, *, full_page=True):
        Path(path).write_bytes(b"synthetic evidence")


def work(document_id):
    return SimpleNamespace(
        portal_id=3, document_id=document_id,
        entry_url="https://srienlinea.sri.gob.ec" + adapter.DOCUMENT_ROUTES[document_id],
        deadline_seconds=2, detail_id=document_id,
        subject=SimpleNamespace(identification=TEST_RUC),
    )


def test_sidecar_uses_document_specific_search_mode_and_selector(tmp_path):
    async def scenario(document_id):
        browser = Browser()
        services = {"browser": browser, "evidence_root": tmp_path}
        await adapter.prepare(work(document_id), services)
        result = await adapter.execute_document(work(document_id), services)
        return browser, result

    for document_id, mode in (
        (3, "Seleccionar búsqueda por RUC o cédula"),
        (53, "Seleccionar búsqueda por RUC"),
    ):
        browser, result = asyncio.run(scenario(document_id))
        assert result["kind"] == "NO_MATCH"
        assert any(action[0] == "goto_commit" for action in browser.actions)
        assert ("mode", mode, True) in browser.actions
        assert ("fill", "#busquedaRucId", "") in browser.actions
        assert ("type", "#busquedaRucId") in browser.actions
        assert any(action[0] == "submit" for action in browser.actions)
        assert ("text", "main") in browser.actions


def test_sidecar_waits_for_spa_controls_after_commit_before_counting(tmp_path):
    class DelayedBrowser(Browser):
        def __init__(self):
            super().__init__()
            self.controls_ready = False

    async def scenario():
        browser = DelayedBrowser()
        services = {"browser": browser, "evidence_root": tmp_path}
        await adapter.prepare(work(3), services)
        result = await adapter.execute_document(work(3), services)
        return browser, result

    browser, result = asyncio.run(scenario())
    assert result["kind"] == "NO_MATCH"
    waits = [action for action in browser.actions if action[0] == "wait_for_selector"]
    assert len(waits) == 2
    assert "#busquedaRucId" in waits[0][1]
    assert waits[0][2] == {"state": "visible", "timeout": 2000}
    assert waits[1][1] == "#busquedaRucId"
    mode_action = ("mode", "Seleccionar búsqueda por RUC o cédula", True)
    assert browser.actions.index(waits[0]) < browser.actions.index(mode_action)


def test_sidecar_fails_closed_when_search_field_is_ambiguous(tmp_path):
    class AmbiguousBrowser(Browser):
        async def count(self, selector):
            if selector == "#busquedaRucId":
                return 2
            return await super().count(selector)

    async def scenario():
        browser = AmbiguousBrowser()
        services = {"browser": browser, "evidence_root": tmp_path}
        await adapter.prepare(work(3), services)
        return browser, await adapter.execute_document(work(3), services)

    browser, result = asyncio.run(scenario())
    assert result == {"kind": "RETRYABLE", "reason_code": "EXPECTED_FIELD_NOT_UNIQUE"}
    assert not any(action[0] == "submit" for action in browser.actions)


def test_legacy_sidecar_falls_back_to_existing_goto_abi(tmp_path):
    class LegacyBrowser(Browser):
        goto_commit = None

    async def scenario():
        browser = LegacyBrowser()
        services = {"browser": browser, "evidence_root": tmp_path}
        await adapter.prepare(work(53), services)
        result = await adapter.execute_document(work(53), services)
        return browser, result

    browser, result = asyncio.run(scenario())
    assert result["kind"] == "NO_MATCH"
    assert any(action[0] == "goto" and action[2] == {"wait_until": "commit"}
               for action in browser.actions)


def test_sidecar_classifies_document_results_and_normalizes_spanish_accents(tmp_path):
    async def scenario(document_id, result_text):
        browser = Browser()
        browser.query_result_text = result_text
        services = {"browser": browser, "evidence_root": tmp_path}
        await adapter.prepare(work(document_id), services)
        result = await adapter.execute_document(work(document_id), services)
        return browser, result

    for document_id, result_text in (
        (3, f"RUC {TEST_RUC}; Estado tributario: AL DÍA EN SUS OBLIGACIONES"),
        (53, f"RUC {TEST_RUC}; Estado del contribuyente: ACTIVO"),
    ):
        browser, result = asyncio.run(scenario(document_id, result_text))
        assert result["kind"] == "MATCH"
        assert Path(result["evidence_path"]).is_file()
        assert ("text", "main") in browser.actions


def test_positive_heading_without_subject_identifier_stays_reintetable(tmp_path):
    async def scenario():
        browser = Browser()
        browser.query_result_text = "Estado tributario: AL DÍA EN SUS OBLIGACIONES"
        services = {"browser": browser, "evidence_root": tmp_path}
        await adapter.prepare(work(3), services)
        return browser, await adapter.execute_document(work(3), services)

    browser, result = asyncio.run(scenario())
    assert result == {"kind": "RETRYABLE", "reason_code": "MATCH_NOT_ATTRIBUTED"}
    assert not list(tmp_path.glob("*.png"))
    assert ("text", "main") in browser.actions


def test_static_help_copy_present_before_query_is_not_a_result(tmp_path):
    async def scenario():
        browser = Browser()
        browser.result_text = "Conozca si se encuentra AL DÍA EN SUS OBLIGACIONES"
        browser.query_result_text = browser.result_text
        services = {"browser": browser, "evidence_root": tmp_path}
        await adapter.prepare(work(3), services)
        return browser, await adapter.execute_document(work(3), services)

    browser, result = asyncio.run(scenario())
    assert result == {"kind": "RETRYABLE", "reason_code": "RESULT_NOT_CONCLUSIVE"}
    assert not list(tmp_path.glob("*.png"))


def test_loading_overlay_defers_result_classification(tmp_path):
    async def scenario():
        browser = Browser()
        browser.query_result_text = "Espere por favor. Estado: AL DÍA EN SUS OBLIGACIONES"
        services = {"browser": browser, "evidence_root": tmp_path}
        await adapter.prepare(work(3), services)
        return browser, await adapter.execute_document(work(3), services)

    _browser, result = asyncio.run(scenario())
    assert result == {"kind": "RETRYABLE", "reason_code": "RESULT_NOT_CONCLUSIVE"}

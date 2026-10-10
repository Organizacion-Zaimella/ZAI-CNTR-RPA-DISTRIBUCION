"""Regresión sintética del ABI SRI; no abre el portal ni usa datos reales."""
from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace


ADAPTER_PATH = Path(__file__).resolve().parents[1] / "src" / "adapter.py"
SPEC = importlib.util.spec_from_file_location("sri_sidecar_under_test", ADAPTER_PATH)
adapter = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = adapter
SPEC.loader.exec_module(adapter)


class Browser:
    def __init__(self):
        self.actions = []
        self.value = ""

    async def goto(self, url, **options):
        self.actions.append(("goto", url, options))

    async def goto_commit(self, url):
        self.actions.append(("goto_commit", url))

    async def is_visible(self, selector):
        return False

    async def count(self, selector):
        if "Seleccionar búsqueda" in selector:
            return 1
        if selector == "#busquedaRucId":
            return 1
        return 0

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

    async def text(self, selector):
        return "No se encontraron resultados"

    async def screenshot(self, path, *, full_page=True):
        Path(path).write_bytes(b"synthetic evidence")


def work(document_id):
    return SimpleNamespace(
        portal_id=3, document_id=document_id,
        entry_url="https://srienlinea.sri.gob.ec" + adapter.DOCUMENT_ROUTES[document_id],
        deadline_seconds=10, detail_id=document_id,
        subject=SimpleNamespace(identification="QA-ONLY"),
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
    assert any(action[0] == "goto" and action[2] == {} for action in browser.actions)

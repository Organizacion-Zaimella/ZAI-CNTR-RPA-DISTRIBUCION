"""Pruebas sintéticas del ABI; no acceden al portal ni contienen sujetos."""
from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace


MODULE = Path(__file__).resolve().parents[1] / "src" / "adapter.py"
SPEC = importlib.util.spec_from_file_location("ofac_sidecar_candidate", MODULE)
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


def work(detail_id, *, url="https://sanctionssearch.ofac.treas.gov/Search.aspx"):
    return SimpleNamespace(portal_id=5, document_id=5, detail_id=detail_id,
                           entry_url=url, deadline_seconds=10,
                           subject=SimpleNamespace(display_name="TEST ONLY"))


class Browser:
    def __init__(self):
        self.goto_calls = 0
        self.actions = []

    async def goto(self, url):
        self.goto_calls += 1
        self.actions.append("goto")
        if self.goto_calls == 1:
            raise RuntimeError("net::ERR_INTERNET_DISCONNECTED https://private.invalid/123")

    async def is_visible(self, selector):
        return False

    async def fill_role(self, *args, **kwargs):
        self.actions.append("fill")

    async def click_role(self, *args, **kwargs):
        self.actions.append("submit")

    async def text(self, selector):
        return "Lookup Results: 0 Found"

    async def screenshot(self, path, *, full_page=True):
        Path(path).write_bytes(b"synthetic screenshot")


def test_network_loss_is_retryable_and_following_work_uses_same_browser(tmp_path):
    browser = Browser()
    services = {"browser": browser, "evidence_root": tmp_path}

    async def scenario():
        await adapter.prepare(work(1), services)
        first = await adapter.documento_5(work(1), services)
        second = await adapter.documento_5(work(2), services)
        return first, second

    first, second = asyncio.run(scenario())
    assert first == {"kind": "RETRYABLE", "reason_code": "NETWORK_DISCONNECTED"}
    assert second["kind"] == "NO_MATCH"
    assert browser.goto_calls == 2
    assert browser.actions == ["goto", "goto", "fill", "submit"]
    assert "private.invalid" not in str(first)


def test_wrong_host_fails_closed_before_browser_navigation():
    class NeverUseBrowser:
        async def goto(self, _url):
            raise AssertionError("unexpected navigation")

    result = asyncio.run(adapter.documento_5(
        work(1, url="https://example.invalid/Search.aspx"),
        {"browser": NeverUseBrowser()}))
    assert result == {"kind": "ERROR", "reason_code": "UNAUTHORIZED_ENTRY_URL"}

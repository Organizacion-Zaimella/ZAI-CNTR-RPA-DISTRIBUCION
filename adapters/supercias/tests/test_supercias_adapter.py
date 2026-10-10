"""Pruebas sintéticas de barrera humana y timeout; no acceden a Supercias."""
from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace



ADAPTER_PATH = Path(__file__).resolve().parents[1] / "adapter.py"
SPEC = importlib.util.spec_from_file_location("supercias_adapter_under_test", ADAPTER_PATH)
adapter = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = adapter
SPEC.loader.exec_module(adapter)


class FakeBrowser:
    def __init__(self, *, challenge=False, timeout=False):
        self.challenge = challenge
        self.timeout = timeout
        self.actions = []

    async def count(self, selector):
        return int(self.challenge)

    async def is_visible(self, selector):
        return self.challenge

    async def goto(self, url):
        self.actions.append(("goto", url))
        if self.timeout:
            raise adapter.PlaywrightTimeoutError("private portal response")


class LateChallengeBrowser(FakeBrowser):
    async def goto(self, url):
        self.actions.append(("goto", url))
        self.challenge = True


def work(document_id=13):
    return SimpleNamespace(
        portal_id=1, document_id=document_id,
        entry_url="https://appscvsgen.supercias.gob.ec/consulta/",
        deadline_seconds=10, execution_id=1, detail_id=document_id,
        subject=SimpleNamespace(id=7, type=SimpleNamespace(value="EMPRESA"),
                                identification="TEST-ONLY", display_name="TEST ONLY"),
    )


def run(coro):
    return asyncio.run(coro)


def test_visible_altcha_stops_without_clicking_or_navigating(tmp_path):
    browser = FakeBrowser(challenge=True)
    result = run(adapter.documento_13(work(), {"browser": browser, "evidence_root": tmp_path}))
    assert result == {"kind": "HUMAN_REQUIRED", "checkpoint": "SUPERCIAS_ENTRY"}
    assert browser.actions == []


def test_portal_timeout_is_retryable_and_sanitized(tmp_path):
    browser = FakeBrowser(timeout=True)
    services = {"browser": browser, "evidence_root": tmp_path}

    async def scenario():
        await adapter.prepare(work(), services)
        return await adapter.documento_13(work(), services)

    result = run(scenario())
    assert result == {"kind": "RETRYABLE", "reason_code": "PORTAL_TIMEOUT"}
    assert len(browser.actions) == 1
    assert "private portal response" not in str(result)


def test_altcha_latch_skips_other_documents_in_same_sidecar_batch(tmp_path):
    browser = LateChallengeBrowser()
    services = {"browser": browser, "evidence_root": tmp_path}

    async def scenario():
        await adapter.prepare(work(), services)
        first = await adapter.documento_13(work(13), services)
        second = await adapter.documento_14(work(14), services)
        return first, second

    first, second = run(scenario())

    assert first["kind"] == "HUMAN_REQUIRED"
    assert second["kind"] == "HUMAN_REQUIRED"
    assert second["reason_code"] == "PORTAL_CHALLENGE"
    assert [action for action, _ in browser.actions] == ["goto"]

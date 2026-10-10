"""Pruebas locales sintéticas; no abren el portal ni crean ejecuciones ORDS."""
from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch


ADAPTER = Path(__file__).resolve().parents[1] / "adapter.py"
spec = importlib.util.spec_from_file_location("judicial_adapter_under_test", ADAPTER)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class Browser:
    def __init__(self, state):
        self.state = state
        self.actions = []
        self.value = ""

    async def goto(self, url, **kwargs):
        self.actions.append(("goto", url))

    async def wait_for_selector(self, selector, **kwargs):
        return None

    async def fill(self, selector, value):
        self.value = value
        self.actions.append(("fill", selector))

    async def input_value(self, selector):
        return self.value

    async def click(self, selector):
        self.actions.append(("click", selector))

    async def is_visible(self, selector):
        return self.state == "challenge"

    async def count(self, selector):
        return 1 if self.state == "match" else 0

    async def text(self, selector):
        if "nth=0" in selector:
            return "Proceso 01/02/2020, resultado válido"
        return "No se encontraron resultados" if self.state == "negative" else "Consulta"

    async def screenshot(self, path, *, full_page):
        assert full_page is True
        Path(path).write_bytes(b"synthetic-png-test-only")


class TimeoutBrowser(Browser):
    async def goto(self, url, **kwargs):
        self.actions.append(("goto", url))
        raise adapter.PlaywrightTimeoutError("synthetic portal timeout")


class PendingBrowser(Browser):
    def __init__(self):
        super().__init__("pending")

    async def search_idle(self):
        return False


class IdleQueueBrowser(PendingBrowser):
    def __init__(self, state="pending"):
        super().__init__()
        self.state = state
        self.idle_checks = 0

    async def search_idle(self):
        self.idle_checks += 1
        return True


class LateChallengeBrowser(Browser):
    async def click(self, selector):
        await super().click(selector)
        self.state = "challenge"


class ChallengeAfterFillBrowser(Browser):
    async def fill(self, selector, value):
        await super().fill(selector, value)
        self.state = "challenge"


def work(document_id, *, entry_url="https://consultas.funcionjudicial.gob.ec/informacionjudicial/public/informacion.jsf"):
    return SimpleNamespace(
        portal_id=6, document_id=document_id, entry_url=entry_url,
        execution_id=1, detail_id=document_id, deadline_seconds=10,
        subject=SimpleNamespace(identification="QA-ONLY", display_name="QA ONLY"),
    )


class AdapterTests(unittest.IsolatedAsyncioTestCase):
    async def test_positive_and_negative_are_distinct(self):
        with tempfile.TemporaryDirectory() as root:
            for state, expected in (("match", "MATCH"), ("negative", "NO_MATCH")):
                browser = Browser(state)
                await adapter.prepare(work(73), {"browser": browser, "evidence_root": root})
                result = await adapter.execute_document(work(73), {"browser": browser, "evidence_root": root})
                self.assertEqual(result["kind"], expected)
                self.assertFalse(result["recovery_click_used"])
                self.assertTrue(Path(result["evidence_path"]).is_file())
                self.assertEqual([name for name, _ in browser.actions], ["goto", "fill", "click"])

    async def test_challenge_never_claims_negative(self):
        with tempfile.TemporaryDirectory() as root:
            browser = Browser("challenge")
            services = {"browser": browser, "evidence_root": root}
            await adapter.prepare(work(74), services)
            result = await adapter.execute_document(work(74), services)
            self.assertEqual(result["kind"], "HUMAN_REQUIRED")
            self.assertEqual(result["checkpoint"], "JUDICIAL_SEARCH")
            self.assertNotIn("evidence_path", result)

    async def test_challenge_appearing_after_fill_blocks_search_click(self):
        with tempfile.TemporaryDirectory() as root:
            browser = ChallengeAfterFillBrowser("ready")
            services = {"browser": browser, "evidence_root": root}
            await adapter.prepare(work(73), services)
            result = await adapter.execute_document(work(73), services)
            self.assertEqual(result["kind"], "HUMAN_REQUIRED")
            self.assertEqual(result["reason_code"], "RECAPTCHA_VISIBLE")
            self.assertEqual([name for name, _ in browser.actions], ["goto", "fill"])

    async def test_captcha_barrier_skips_rest_of_same_portal_batch(self):
        with tempfile.TemporaryDirectory() as root:
            browser = LateChallengeBrowser("ready")
            services = {"browser": browser, "evidence_root": root}
            await adapter.prepare(work(73), services)
            first = await adapter.execute_document(work(73), services)
            second = await adapter.execute_document(work(74), services)
            self.assertEqual(first["kind"], "HUMAN_REQUIRED")
            self.assertEqual(second["kind"], "HUMAN_REQUIRED")
            self.assertEqual(second["reason_code"], "PORTAL_CHALLENGE")
            self.assertEqual([name for name, _ in browser.actions], ["goto", "fill", "click"])

    async def test_navigation_timeout_is_retryable_and_keeps_browser_session(self):
        browser = TimeoutBrowser("negative")
        services = {"browser": browser, "evidence_root": "."}
        await adapter.prepare(work(73), services)
        result = await adapter.execute_document(work(73), services)
        self.assertEqual(result, {"kind": "RETRYABLE", "reason_code": "PORTAL_TIMEOUT"})
        self.assertEqual([name for name, _ in browser.actions], ["goto"])

    async def test_pending_result_never_repeats_public_search_submission(self):
        class Clock:
            now = 0.0

            def time(self):
                return self.now

        clock = Clock()

        async def advance(seconds):
            clock.now += seconds

        item = work(73)
        item.deadline_seconds = 7
        browser = PendingBrowser()
        services = {"browser": browser, "evidence_root": "."}
        await adapter.prepare(item, services)
        with patch.object(adapter.asyncio, "get_running_loop", return_value=clock), \
                patch.object(adapter.asyncio, "sleep", side_effect=advance):
            result = await adapter.execute_document(item, services)
        self.assertEqual(result["kind"], "RETRYABLE")
        self.assertEqual(result["reason_code"], "RESULT_UNVERIFIED")
        self.assertFalse(result["recovery_click_used"])
        self.assertEqual([name for name, _ in browser.actions], ["goto", "fill", "click"])

    async def test_idle_jsf_queue_allows_exactly_one_bounded_recovery_click(self):
        class Clock:
            now = 0.0

            def time(self):
                return self.now

        clock = Clock()

        async def advance(seconds):
            clock.now += seconds

        item = work(74)
        item.deadline_seconds = 8
        browser = IdleQueueBrowser()
        services = {"browser": browser, "evidence_root": "."}
        await adapter.prepare(item, services)
        with patch.object(adapter.asyncio, "get_running_loop", return_value=clock), \
                patch.object(adapter.asyncio, "sleep", side_effect=advance):
            result = await adapter.execute_document(item, services)
        self.assertEqual(result["kind"], "RETRYABLE")
        self.assertEqual(result["reason_code"], "RESULT_UNVERIFIED")
        self.assertTrue(result["recovery_click_used"])
        self.assertEqual([name for name, _ in browser.actions],
                         ["goto", "fill", "click", "click"])
        self.assertEqual(browser.idle_checks, 1)

    async def test_rejects_unapproved_entry_url(self):
        with tempfile.TemporaryDirectory() as root:
            result = await adapter.execute_document(
                work(75, entry_url="https://example.invalid/"),
                {"browser": Browser("match"), "evidence_root": root},
            )
            self.assertEqual(result["kind"], "ERROR")
            self.assertEqual(result["reason_code"], "ENTRY_URL_INVALID")

    async def test_supported_documents_use_correct_subject_field(self):
        with tempfile.TemporaryDirectory() as root:
            for document_id in (73, 74, 75, 76):
                browser = Browser("negative")
                services = {"browser": browser, "evidence_root": root}
                await adapter.prepare(work(document_id), services)
                result = await adapter.execute_document(work(document_id), services)
                self.assertEqual(result["kind"], "NO_MATCH")
                expected = "QA-ONLY" if document_id in (73, 74) else "QA ONLY"
                self.assertEqual(browser.value, expected)


if __name__ == "__main__":
    unittest.main()

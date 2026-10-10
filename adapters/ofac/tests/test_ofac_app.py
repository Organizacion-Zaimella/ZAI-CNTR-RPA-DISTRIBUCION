"""Pruebas sintéticas de continuidad de lote; no acceden a OFAC."""
from __future__ import annotations

import asyncio
import hashlib
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
SPEC = importlib.util.spec_from_file_location("ofac_standalone_app", APP_PATH)
app = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = app
SPEC.loader.exec_module(app)


class Locator:
    def __init__(self, page, selector):
        self.page, self.selector = page, selector

    async def count(self):
        return 1

    async def fill(self, value, **kwargs):
        self.page.actions.append(("fill", value))

    async def click(self, **kwargs):
        self.page.actions.append(("click", self.selector))
        if self.page.challenge_after_search:
            self.page.body = "Verify you are human"

    async def inner_text(self):
        return self.page.body


class Page:
    def __init__(self, first_navigation_timeout=False, first_navigation_error=None,
                 status=200, body="Lookup Results: 0 Found", challenge_after_search=False):
        self.first_navigation_timeout = first_navigation_timeout
        self.first_navigation_error = first_navigation_error
        self.status = status
        self.body = body
        self.challenge_after_search = challenge_after_search
        self.navigations = 0
        self.actions = []

    async def goto(self, url, **kwargs):
        self.navigations += 1
        if self.first_navigation_timeout and self.navigations == 1:
            raise app.PlaywrightTimeoutError("synthetic timeout")
        if self.first_navigation_error and self.navigations == 1:
            raise RuntimeError(self.first_navigation_error)
        return SimpleNamespace(status=self.status)

    def locator(self, selector):
        return Locator(self, selector)

    def get_by_role(self, role, **kwargs):
        return Locator(self, role)

    async def wait_for_timeout(self, ms):
        return None

    async def screenshot(self, *, path, full_page):
        Path(path).write_bytes(b"synthetic-png-test-only")


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

    async def click_role(self, *args, **kwargs):
        self.actions.append("click")
        self.challenge = True

    async def text(self, selector):
        return "Verify you are human"


class Browser:
    def __init__(self, page):
        self.page = page
        self.new_page_calls = 0
        self.close_calls = 0

    async def new_page(self):
        self.new_page_calls += 1
        return self.page

    async def close(self):
        self.close_calls += 1


class PlaywrightContext:
    def __init__(self, browser):
        self.chromium = SimpleNamespace(launch=self.launch)
        self.browser = browser
        self.launch_calls = 0

    async def launch(self, **kwargs):
        self.launch_calls += 1
        return self.browser

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None


def context(evidence_dir: Path):
    return {"url": "https://sanctionssearch.ofac.treas.gov/", "name": "TEST ONLY",
            "evidence_dir": evidence_dir, "timeout": 1, "pacing": 0}


def work(detail_id):
    return SimpleNamespace(portal_id=5, document_id=5, detail_id=detail_id,
                           entry_url="https://sanctionssearch.ofac.treas.gov/",
                           deadline_seconds=10,
                           subject=SimpleNamespace(display_name="TEST ONLY"))


def run(coro):
    return asyncio.run(coro)


def test_timeout_advances_to_next_case_in_same_browser_session(tmp_path, monkeypatch):
    page = Page(first_navigation_timeout=True)
    browser = Browser(page)
    playwright = PlaywrightContext(browser)
    monkeypatch.setattr(app, "async_playwright", lambda: playwright)

    results = run(app.run_many([context(tmp_path), context(tmp_path)]))

    assert [item["status"] for item in results] == ["RETRYABLE", "NO_MATCH"]
    assert [item["reason_code"] for item in results] == ["PORTAL_NAVIGATION_TIMEOUT", None]
    assert page.navigations == 2
    assert browser.new_page_calls == 1
    assert browser.close_calls == 1


def test_internet_disconnect_is_sanitized_and_next_case_uses_same_page(tmp_path, monkeypatch):
    page = Page(first_navigation_error=(
        "net::ERR_INTERNET_DISCONNECTED https://private.invalid/subject/123"))
    browser = Browser(page)
    playwright = PlaywrightContext(browser)
    monkeypatch.setattr(app, "async_playwright", lambda: playwright)

    results = run(app.run_many([context(tmp_path), context(tmp_path)]))

    assert [item["status"] for item in results] == ["RETRYABLE", "NO_MATCH"]
    assert [item["reason_code"] for item in results] == ["NETWORK_DISCONNECTED", None]
    assert "private.invalid" not in str(results)
    assert page.navigations == 2
    assert browser.new_page_calls == 1
    assert browser.close_calls == 1


def test_http_restriction_stops_batch_without_second_navigation(tmp_path, monkeypatch):
    page = Page(status=403)
    browser = Browser(page)
    playwright = PlaywrightContext(browser)
    monkeypatch.setattr(app, "async_playwright", lambda: playwright)

    results = run(app.run_many([context(tmp_path), context(tmp_path)]))

    assert [item["status"] for item in results] == ["BLOCKED"]
    assert results[0]["reason_code"] == "HTTP_403"
    assert page.navigations == 1
    assert browser.new_page_calls == 1
    assert browser.close_calls == 1


def test_positive_result_saves_full_page_evidence_and_hash(tmp_path, monkeypatch):
    page = Page(body="Lookup Results: 2 Found")
    browser = Browser(page)
    playwright = PlaywrightContext(browser)
    monkeypatch.setattr(app, "async_playwright", lambda: playwright)

    results = run(app.run_many([context(tmp_path)]))

    assert len(results) == 1
    assert results[0]["status"] == "MATCH"
    assert results[0]["evidence_type"] == "PNG"
    evidence = next(tmp_path.glob("ofac-document-5-*.png"))
    assert results[0]["evidence_sha256"] == hashlib.sha256(evidence.read_bytes()).hexdigest()


def test_challenge_after_search_stops_batch_without_requery(tmp_path, monkeypatch):
    page = Page(challenge_after_search=True)
    browser = Browser(page)
    playwright = PlaywrightContext(browser)
    monkeypatch.setattr(app, "async_playwright", lambda: playwright)

    results = run(app.run_many([context(tmp_path), context(tmp_path)]))

    assert [item["status"] for item in results] == ["HUMAN_REQUIRED"]
    assert results[0]["reason_code"] == "PORTAL_CHALLENGE"
    assert page.navigations == 1
    assert [action[0] for action in page.actions] == ["fill", "click"]
    assert browser.new_page_calls == 1
    assert browser.close_calls == 1


def test_sidecar_challenge_latch_skips_remaining_details_without_navigation(tmp_path):
    browser = SidecarBrowser()
    services = {"browser": browser, "evidence_root": tmp_path}

    async def scenario():
        await app.prepare(work(1), services)
        first = await app.documento_5(work(1), services)
        second = await app.documento_5(work(2), services)
        return first, second

    first, second = run(scenario())

    assert first["kind"] == "HUMAN_REQUIRED"
    assert second["kind"] == "HUMAN_REQUIRED"
    assert browser.actions == ["goto", "fill", "click"]

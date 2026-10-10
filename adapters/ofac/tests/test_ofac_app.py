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

    async def wait_for(self, **kwargs):
        self.page.ready_checks.append((self.selector, kwargs))

    async def fill(self, value, **kwargs):
        self.page.actions.append(("fill", value))

    async def click(self, **kwargs):
        self.page.actions.append(("click", self.selector))
        if self.page.challenge_after_search:
            self.page.body = "Verify you are human"

    async def inner_text(self):
        if self.page.body_sequence:
            return self.page.body_sequence.pop(0)
        return self.page.body


class Page:
    def __init__(self, first_navigation_timeout=False, first_navigation_error=None,
                 status=200, body="Lookup Results: 0 Found", challenge_after_search=False):
        self.first_navigation_timeout = first_navigation_timeout
        self.first_navigation_error = first_navigation_error
        self.status = status
        self.body = body
        self.challenge_after_search = challenge_after_search
        self.body_sequence = []
        self.navigations = 0
        self.navigation_options = []
        self.actions = []
        self.waits = []
        self.ready_checks = []

    async def goto(self, url, **kwargs):
        self.navigations += 1
        self.navigation_options.append(kwargs)
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
        self.waits.append(ms)
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
    assert len(page.ready_checks) == 2


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


def test_http_429_stops_batch_without_repeating_request(tmp_path, monkeypatch):
    page = Page(status=429)
    browser = Browser(page)
    playwright = PlaywrightContext(browser)
    monkeypatch.setattr(app, "async_playwright", lambda: playwright)

    results = run(app.run_many([context(tmp_path), context(tmp_path)]))

    assert [item["status"] for item in results] == ["BLOCKED"]
    assert results[0]["reason_code"] == "HTTP_429"
    assert page.navigations == 1
    assert browser.new_page_calls == 1
    assert browser.close_calls == 1


def test_challenge_before_form_entry_never_submits_name(tmp_path, monkeypatch):
    page = Page(body="Verify you are human")
    browser = Browser(page)
    playwright = PlaywrightContext(browser)
    monkeypatch.setattr(app, "async_playwright", lambda: playwright)

    results = run(app.run_many([context(tmp_path), context(tmp_path)]))

    assert [item["status"] for item in results] == ["HUMAN_REQUIRED"]
    assert results[0]["reason_code"] == "PORTAL_CHALLENGE"
    assert page.actions == []
    assert page.navigations == 1


def test_missing_result_count_remains_retryable_without_evidence(tmp_path, monkeypatch):
    page = Page(body="Search submitted; results are still loading")
    browser = Browser(page)
    playwright = PlaywrightContext(browser)
    monkeypatch.setattr(app, "async_playwright", lambda: playwright)
    item = context(tmp_path)
    item["timeout"] = 0.01

    results = run(app.run_many([item]))

    assert results[0]["status"] == "RETRYABLE"
    assert results[0]["reason_code"] == "RESULT_COUNT_NOT_CONCLUSIVE"
    assert results[0]["evidence_sha256"] is None
    assert list(tmp_path.iterdir()) == []


def test_loading_overlay_defers_even_when_old_result_count_is_present(tmp_path, monkeypatch):
    page = Page(body="Please wait... Lookup Results: 0 Found")
    browser = Browser(page)
    playwright = PlaywrightContext(browser)
    monkeypatch.setattr(app, "async_playwright", lambda: playwright)
    item = context(tmp_path)
    item["timeout"] = 0.01

    results = run(app.run_many([item]))

    assert results[0]["status"] == "RETRYABLE"
    assert results[0]["reason_code"] == "RESULT_COUNT_NOT_CONCLUSIVE"
    assert page.waits.count(500) >= 1
    assert list(tmp_path.iterdir()) == []


def test_result_count_must_be_stable_across_two_observations(tmp_path, monkeypatch):
    page = Page(body="Form ready")
    page.body_sequence = ["Form ready", "Lookup Results: 1 Found",
                          "Lookup Results: 0 Found", "Lookup Results: 0 Found"]
    browser = Browser(page)
    playwright = PlaywrightContext(browser)
    monkeypatch.setattr(app, "async_playwright", lambda: playwright)

    results = run(app.run_many([context(tmp_path)]))

    assert results[0]["status"] == "NO_MATCH"
    assert page.waits.count(500) >= 2


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


def test_navigation_controls_and_results_have_separate_wait_budgets(tmp_path, monkeypatch):
    page = Page(body="Lookup Results: 0 Found")
    browser = Browser(page)
    playwright = PlaywrightContext(browser)
    monkeypatch.setattr(app, "async_playwright", lambda: playwright)
    item = context(tmp_path)
    item.update({"timeout": 120, "navigation_timeout": 30,
                 "control_timeout": 30, "result_timeout": 120})

    result = run(app.run_many([item]))[0]

    assert result["status"] == "NO_MATCH"
    assert page.navigation_options[0]["wait_until"] == "domcontentloaded"
    assert page.navigation_options[0]["timeout"] == 30_000
    assert all(options["timeout"] == 30_000 for _, options in page.ready_checks)
    assert app.RESULT_INITIAL_TIMEOUT_SECONDS == 60
    assert app.RESULT_EXTENSION_SECONDS == 30
    assert app.RESULT_MAX_TIMEOUT_SECONDS == 120


def test_search_deadline_extends_only_with_progress_and_never_past_cap():
    assert app._extend_result_deadline(60, 120, 60, False) == 60
    assert app._extend_result_deadline(60, 120, 60, True) == 90
    assert app._extend_result_deadline(100, 120, 105, True) == 120


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


def test_sidecar_waits_for_result_count_to_stabilize(tmp_path):
    class ResultBrowser:
        def __init__(self):
            self.actions = []
            self.texts = iter(["Lookup Results: 1 Found",
                               "Lookup Results: 0 Found",
                               "Lookup Results: 0 Found"])

        async def goto(self, _url):
            self.actions.append("goto")

        async def is_visible(self, _selector):
            return False

        async def fill_role(self, *_args, **_kwargs):
            self.actions.append("fill")

        async def click_role(self, *_args, **_kwargs):
            self.actions.append("submit")

        async def text(self, _selector):
            self.actions.append("read_result")
            return next(self.texts)

        async def screenshot(self, path, *, full_page):
            Path(path).write_bytes(b"synthetic evidence")

    async def scenario():
        browser = ResultBrowser()
        test_work = work(90)
        services = {"browser": browser, "evidence_root": tmp_path}
        await app.prepare(test_work, services)
        result = await app.documento_5(test_work, services)
        return browser, result

    browser, result = run(scenario())

    assert result["kind"] == "NO_MATCH"
    assert browser.actions.count("read_result") == 3
    assert Path(result["evidence_path"]).is_file()

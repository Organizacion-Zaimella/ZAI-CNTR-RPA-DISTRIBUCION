"""Pruebas locales del runner standalone; no consultan el portal ni ORDS."""
from __future__ import annotations

import asyncio
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
SPEC = importlib.util.spec_from_file_location("judicatura_standalone_app_test", APP_PATH)
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
        self.launches = []
        self.chromium = SimpleNamespace(launch=self.launch)

    async def launch(self, **kwargs):
        self.launches.append(kwargs)
        return self.browser

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return None


def make_work(document_id):
    return SimpleNamespace(document_id=document_id, portal_id=6)


def test_context_keeps_the_received_document_order_and_private_paths(tmp_path):
    repo_context = tmp_path / "context.json"
    evidence = tmp_path / "evidence"
    repo_context.write_text(json.dumps({
        "portal_id": 6,
        "evidence_dir": str(evidence),
        "works": [
            {"document_id": 74, "entry_url": "https://consultas.funcionjudicial.gob.ec/informacionjudicial/public/informacion.jsf",
             "execution_id": 1, "detail_id": 2,
             "subject": {"identification": "local-test", "display_name": "Local Test"}},
            {"document_id": 73, "entry_url": "https://consultas.funcionjudicial.gob.ec/informacionjudicial/public/informacion.jsf",
             "execution_id": 1, "detail_id": 3,
             "subject": {"identification": "local-test", "display_name": "Local Test"}},
        ],
    }), encoding="utf-8")

    works, root = app.load_context(repo_context)

    assert [work.document_id for work in works] == [74, 73]
    assert root == evidence.resolve()


def test_standalone_context_uses_local_correlation_without_fabricating_ords_ids(tmp_path):
    context = tmp_path / "context.json"
    context.write_text(json.dumps({
        "portal_id": 6,
        "standalone_mode": True,
        "evidence_dir": str(tmp_path / "evidence"),
        "works": [{
            "document_id": 73,
            "entry_url": "https://consultas.funcionjudicial.gob.ec/informacionjudicial/public/informacion.jsf",
            "subject": {"identification": "local-private", "display_name": "Local Private"},
        }],
    }), encoding="utf-8")

    works, _ = app.load_context(context)

    assert works[0].execution_id == "standalone"
    assert works[0].detail_id == "73-001"


def test_standalone_evidence_names_are_unique_across_documents(tmp_path):
    context = tmp_path / "context.json"
    context.write_text(json.dumps({
        "portal_id": 6,
        "standalone_mode": True,
        "evidence_dir": str(tmp_path / "evidence"),
        "works": [
            {"document_id": document_id,
             "entry_url": "https://consultas.funcionjudicial.gob.ec/informacionjudicial/public/informacion.jsf",
             "subject": {"identification": "local-private", "display_name": "Local Private"}}
            for document_id in (73, 74)
        ],
    }), encoding="utf-8")

    works, _ = app.load_context(context)

    names = [f"judicial-{work.execution_id}-{work.detail_id}.png" for work in works]
    assert names == ["judicial-standalone-73-001.png", "judicial-standalone-74-002.png"]
    assert len(set(names)) == len(names)


def test_runner_keeps_one_browser_page_and_continues_after_isolated_failure(tmp_path, monkeypatch):
    playwright = Playwright()
    monkeypatch.setattr(app, "async_playwright", lambda: playwright)
    seen = []

    async def prepare(_work, _services):
        return None

    async def execute(work, services):
        seen.append((work.document_id, id(services["browser"].page)))
        if work.document_id == 74:
            raise TimeoutError("private exception text")
        return {"kind": "NO_MATCH"}

    monkeypatch.setattr(app.adapter, "prepare", prepare)
    monkeypatch.setattr(app.adapter, "execute_document", execute)

    results = asyncio.run(app.run_context(
        [make_work(74), make_work(73)], tmp_path, headless=True))

    assert [item["status"] for item in results] == ["RETRYABLE", "NO_MATCH"]
    assert [item[0] for item in seen] == [74, 73]
    assert seen[0][1] == seen[1][1]
    assert len(playwright.browser.pages) == 1
    assert playwright.browser.close_calls == 1

"""Contrato del módulo dinámico; sin red, sujetos reales ni ORDS."""
from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace

import importlib.util

ADAPTER_PATH = Path(__file__).resolve().parents[1] / "src" / "adapter.py"
SPEC = importlib.util.spec_from_file_location("iess_sidecar_adapter", ADAPTER_PATH)
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


def pdf_bytes() -> bytes:
    return b"%PDF-1.4\n" + b"x" * 128 + b"\nstartxref\n0\n%%EOF\n"


class Browser:
    def __init__(self, *, pdf=pdf_bytes(), challenge=False, timeout=False,
                 download_timeout=False):
        self.pdf = pdf
        self.challenge = challenge
        self.timeout = timeout
        self.download_timeout = download_timeout
        self.value = None
        self.actions = []

    async def goto(self, url):
        self.actions.append(("goto", url))
        if self.timeout:
            raise TimeoutError("synthetic timeout with private URL")

    async def is_visible(self, selector):
        self.actions.append(("visible", selector))
        return self.challenge

    async def fill_role(self, role, name, value, **kwargs):
        self.actions.append(("fill", role, name, kwargs))
        self.value = value

    async def download_by_click(self, selector, destination, **kwargs):
        self.actions.append(("download", selector, kwargs))
        if self.download_timeout:
            Path(destination).write_bytes(b"partial")
            raise TimeoutError("synthetic download timeout with private URL")
        Path(destination).write_bytes(self.pdf)


def work(*, portal_id=2, document_id=2):
    return SimpleNamespace(
        portal_id=portal_id, document_id=document_id, detail_id=991,
        entry_url="https://www.iess.gob.ec/fixture",
        subject=SimpleNamespace(identification="SYNTHETIC-ONLY"),
    )


def run(coro):
    return asyncio.run(coro)


def test_sidecar_adapter_acquires_and_validates_native_pdf(tmp_path):
    browser = Browser()
    result = run(adapter.documento_2(work(), {"browser": browser, "evidence_root": tmp_path}))

    assert result == {"kind": "MATCH", "evidence_path": str(tmp_path / "iess-991.pdf")}
    assert browser.actions[2] == ("fill", "textbox", None, {})
    assert browser.actions[-1] == (
        "download", 'button:has-text("CONSULTAR")', {}
    )
    assert adapter.valid_pdf_for_ords(Path(result["evidence_path"]))


def test_sidecar_adapter_rejects_and_removes_invalid_pdf(tmp_path):
    browser = Browser(pdf=b"%PDF-1.4" + b"x" * 200)
    result = run(adapter.documento_2(work(), {"browser": browser, "evidence_root": tmp_path}))

    assert result == {"kind": "RETRYABLE", "reason_code": "NATIVE_PDF_STRUCTURE_INVALID"}
    assert not (tmp_path / "iess-991.pdf").exists()


def test_sidecar_adapter_honors_human_challenge_without_search(tmp_path):
    browser = Browser(challenge=True)
    result = run(adapter.documento_2(work(), {"browser": browser, "evidence_root": tmp_path}))

    assert result == {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
    assert not any(action[0] in {"fill", "click"} for action in browser.actions)


def test_sidecar_adapter_sanitizes_timeout_as_retryable(tmp_path):
    browser = Browser(timeout=True)
    result = run(adapter.documento_2(work(), {"browser": browser, "evidence_root": tmp_path}))

    assert result == {"kind": "RETRYABLE", "reason_code": "NATIVE_PDF_NOT_ACQUIRED"}
    assert "private URL" not in repr(result)


def test_download_timeout_is_retryable_and_does_not_resubmit(tmp_path):
    browser = Browser(download_timeout=True)
    result = run(adapter.documento_2(work(), {"browser": browser, "evidence_root": tmp_path}))

    assert result == {"kind": "RETRYABLE", "reason_code": "NATIVE_PDF_NOT_ACQUIRED"}
    assert [action[0] for action in browser.actions].count("download") == 1
    assert not (tmp_path / "iess-991.pdf").exists()
    assert "private URL" not in repr(result)


def test_sidecar_adapter_rejects_wrong_document_without_navigation(tmp_path):
    browser = Browser()
    result = run(adapter.documento_2(work(document_id=3), {"browser": browser, "evidence_root": tmp_path}))

    assert result == {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    assert browser.actions == []

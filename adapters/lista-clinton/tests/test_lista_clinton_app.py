"""Búsqueda offline del PDF Lista Clinton; no accede a Treasury ni ORDS."""
from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fitz

import app


def pdf_bytes(pages: tuple[str, ...]) -> bytes:
    document = fitz.open()
    for text in pages:
        page = document.new_page()
        if text:
            page.insert_text((72, 72), text)
    content = document.tobytes()
    document.close()
    return content


class Response:
    def __init__(self, body: bytes, status: int = 200):
        self._body, self.status = body, status

    async def body(self):
        return self._body


class Browser:
    def __init__(self, response):
        self.response = response
        self.calls = []

    async def goto(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.response


def work(*, portal=134, document=33, name="ÁCME, Holdings"):
    return SimpleNamespace(portal_id=portal, document_id=document, detail_id=731,
                           entry_url="https://www.treasury.gov/ofac/downloads/sdnlist.pdf",
                           subject=SimpleNamespace(display_name=name))


def test_normalization_ignores_visual_spacing_punctuation_and_accents():
    assert app.normalize("Ácme, Holdings S.A.") == "acmeholdingssa"


def test_url_contract_rejects_unapproved_hosts_and_query_parameters():
    for url in (
        "https://treasury.gov/ofac/downloads/sdnlist.pdf",
        "https://www.treasury.gov/ofac/downloads/sdnlist.pdf?x=1",
        "https://user@www.treasury.gov/ofac/downloads/sdnlist.pdf",
    ):
        try:
            app.validate_url(url)
        except ValueError:
            pass
        else:
            raise AssertionError("URL fuera de contrato aceptada")


def test_match_returns_pdf_receipt_and_preserves_source(tmp_path):
    source = pdf_bytes(("ACME Holdings S.A.\nSource page one", "Other entry"))
    result = app.search_and_bundle(source, "Ácme, Holdings", tmp_path, 731)

    assert result["status"] == "MATCH"
    assert result["match_count"] == 1
    assert result["matched_pages"] == [1]
    artifact = Path(result["evidence_path"])
    assert artifact.read_bytes().startswith(b"%PDF-")
    with fitz.open(artifact) as bundle:
        assert bundle.page_count == 3
        assert "COINCIDENCIA ENCONTRADA" in bundle[0].get_text()
        assert "Source page one" in bundle[1].get_text()


def test_no_match_requires_text_on_every_page(tmp_path):
    source = pdf_bytes(("Non-matching entry", "Another text page"))
    result = app.search_and_bundle(source, "Synthetic Name", tmp_path, 732)

    assert result["status"] == "NO_MATCH"
    assert result["match_count"] == 0
    assert Path(result["evidence_path"]).is_file()

    incomplete = app.search_and_bundle(pdf_bytes(("Searchable page", "")),
                                       "Synthetic Name", tmp_path, 733)
    assert incomplete == {"status": "RETRYABLE", "reason_code": "PDF_TEXT_INCOMPLETE",
                          "pages_without_text": 1}


def test_historical_3229_page_register_completes_and_keeps_bundle_bounded(tmp_path):
    source = fitz.open()
    for index in range(3229):
        page = source.new_page()
        page.insert_text((72, 72), f"Public register entry {index + 1}")
        if index == 2999:
            page.insert_text((72, 90), "Synthetic Test Entity")
    content = source.tobytes()
    source.close()

    result = app.search_and_bundle(content, "Synthetic Test Entity", tmp_path, 734)

    assert result["status"] == "MATCH"
    assert result["pages_checked"] == 3229
    assert result["matched_pages"] == [3000]
    assert Path(result["evidence_path"]).stat().st_size <= app.MAX_PDF_BYTES


def test_sidecar_uses_ords_ordered_identity_and_native_response(tmp_path):
    browser = Browser(Response(pdf_bytes(("ACME Holdings",))))
    result = asyncio.run(app.documento_33(
        work(), {"browser": browser, "evidence_root": tmp_path}))

    assert result["kind"] == "MATCH"
    assert browser.calls == [(work().entry_url, {"wait_until": "commit"})]
    assert Path(result["evidence_path"]).is_file()


def test_sidecar_rejects_wrong_pair_without_navigation(tmp_path):
    browser = Browser(Response(pdf_bytes(("ACME Holdings",))))
    result = asyncio.run(app.documento_33(
        work(document=5), {"browser": browser, "evidence_root": tmp_path}))

    assert result == {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    assert browser.calls == []


def test_sidecar_classifies_403_without_retrying_or_bypassing(tmp_path):
    browser = Browser(Response(b"", status=403))
    result = asyncio.run(app.documento_33(
        work(), {"browser": browser, "evidence_root": tmp_path}))

    assert result == {"kind": "RETRYABLE", "reason_code": "HTTP_403"}
    assert len(browser.calls) == 1


def test_network_disconnect_is_sanitized_and_next_work_uses_same_browser(tmp_path):
    class SequenceBrowser:
        def __init__(self):
            self.calls = []

        async def goto(self, url, **kwargs):
            self.calls.append((url, kwargs))
            if len(self.calls) == 1:
                raise RuntimeError("net::ERR_INTERNET_DISCONNECTED https://private.invalid/subject")
            return Response(pdf_bytes(("ACME Holdings",)))

    browser = SequenceBrowser()
    services = {"browser": browser, "evidence_root": tmp_path}
    first = asyncio.run(app.documento_33(work(), services))
    second = asyncio.run(app.documento_33(work(), services))

    assert first == {"kind": "RETRYABLE", "reason_code": "NETWORK_DISCONNECTED"}
    assert second["kind"] == "MATCH"
    assert len(browser.calls) == 2
    assert "private.invalid" not in repr(first)
    assert "subject" not in repr(first)


def test_network_failure_classification_never_returns_exception_text():
    cases = {
        "net::ERR_NETWORK_CHANGED": "NETWORK_CHANGED",
        "net::ERR_CONNECTION_RESET": "PORTAL_CONNECTION_RESET",
        "net::ERR_NAME_NOT_RESOLVED": "PORTAL_DNS_FAILURE",
        "net::ERR_ADDRESS_UNREACHABLE": "PORTAL_UNREACHABLE",
        "unexpected private content": "PORTAL_UNAVAILABLE",
    }
    for message, expected in cases.items():
        result = app._network_failure_code(RuntimeError(message + " private.invalid"))
        assert result == expected
        assert "private.invalid" not in result


def test_pdf_wait_budget_is_bounded_and_transfer_timeout_is_retryable():
    class SlowResponse:
        async def body(self):
            await asyncio.sleep(1)
            return b"%PDF-"

    assert app.PDF_TOTAL_TIMEOUT_SECONDS == 90
    assert app.NAVIGATION_START_TIMEOUT_SECONDS == 30
    assert app.PDF_TRANSFER_TIMEOUT_SECONDS == 60
    body, failure = asyncio.run(app._read_pdf_body(SlowResponse(), 0.01))
    assert body is None
    assert failure == "PDF_TRANSFER_TIMEOUT"

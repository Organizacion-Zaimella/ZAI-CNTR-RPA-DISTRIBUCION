"""IESS, documento 2: PDF nativo tras consulta, sin generar PDF sintético."""
from __future__ import annotations

from pathlib import Path


async def documento_2(work, services):
    if work.portal_id != 2 or work.document_id != 2:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    browser = services["browser"]
    await browser.goto(work.entry_url)
    if await browser.is_visible('iframe[src*="captcha"], [class*="altcha"]'):
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
    await browser.fill_role("textbox", "", work.subject.identification)
    target = Path(services["evidence_root"]) / f"iess-{work.detail_id}.pdf"
    try:
        await browser.pdf_response_by_click_role("button", "CONSULTAR", str(target))
    except Exception:
        # El portal también puede abrir descarga/pestaña; no fabricar evidencia.
        return {"kind": "RETRYABLE", "reason_code": "PDF_NOT_ACQUIRED"}
    return {"kind": "MATCH", "evidence_path": str(target)}


DOCUMENT_FUNCTIONS = {"documento_2": documento_2}


async def execute_document(work, services):
    return await documento_2(work, services)

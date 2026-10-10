"""SRI, documentos 3/53. Prototipo privado sujeto a verificación visual TEST."""
from __future__ import annotations

import asyncio
from pathlib import Path
import time


async def _execute_document(work, services, expected_document_id):
    if work.portal_id != 3 or work.document_id != expected_document_id:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    browser = services["browser"]
    await browser.goto(work.entry_url)
    if await browser.is_visible('iframe[src*="captcha"], [class*="altcha"]'):
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
    label = "RUC" if work.document_id == 53 else "RUC / cédula"
    await browser.fill_label(label, work.subject.identification)
    await browser.click_role("button", "Consultar")
    deadline = time.monotonic() + min(work.deadline_seconds, 120)
    while time.monotonic() < deadline:
        if await browser.is_visible('iframe[src*="captcha"], [class*="altcha"]'):
            return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
        body = (await browser.text("body")).casefold()
        if "no se encontraron resultados" in body:
            kind = "NO_MATCH"
        elif (work.document_id == 3 and "al dia en sus obligaciones" in body) or \
             (work.document_id == 53 and "activo" in body):
            # El marcador histórico puede existir fuera de la fila del sujeto.
            return {"kind": "RETRYABLE", "reason_code": "MATCH_NOT_ATTRIBUTED"}
        else:
            await asyncio.sleep(0.5)
            continue
        target = Path(services["evidence_root"]) / f"sri-{work.document_id}-{work.detail_id}.png"
        await browser.screenshot(str(target), full_page=True)
        return {"kind": kind, "evidence_path": str(target)}
    return {"kind": "RETRYABLE", "reason_code": "RESULT_NOT_CONCLUSIVE"}


async def documento_3(work, services):
    return await _execute_document(work, services, 3)


async def documento_53(work, services):
    return await _execute_document(work, services, 53)


DOCUMENT_FUNCTIONS = {"documento_3": documento_3, "documento_53": documento_53}


async def execute_document(work, services):
    function = DOCUMENT_FUNCTIONS.get(f"documento_{work.document_id}")
    if function is None:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    return await function(work, services)

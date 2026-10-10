"""SRI, documentos 3/53. Prototipo privado sujeto a verificación visual TEST."""
from __future__ import annotations

import asyncio
from pathlib import Path
import time
from urllib.parse import urlparse

SRI_HOST = "srienlinea.sri.gob.ec"
DOCUMENT_ROUTES = {
    3: "/sri-en-linea/SriDeclaracionesWeb/EstadoTributario/Consultas/consultaEstadoTributario",
    53: "/sri-en-linea/SriRucWeb/ConsultaRuc/Consultas/consultaRuc",
}
_human_barrier = False


async def _execute_document(work, services, expected_document_id):
    global _human_barrier
    if work.portal_id != 3 or work.document_id != expected_document_id:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    if _human_barrier:
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE",
                "reason_code": "PORTAL_CHALLENGE"}
    parsed = urlparse(work.entry_url)
    if (parsed.scheme != "https" or parsed.hostname != SRI_HOST or
            parsed.path.rstrip("/") != DOCUMENT_ROUTES[expected_document_id]):
        return {"kind": "ERROR", "reason_code": "UNAUTHORIZED_ENTRY_URL"}
    browser = services["browser"]
    # Newer generic sidecars expose goto_commit for SPAs. Keep compatibility
    # with the installed 1.0.0 ABI, which only offers goto/domcontentloaded.
    goto_commit = getattr(browser, "goto_commit", None)
    if callable(goto_commit):
        await goto_commit(work.entry_url)
    else:
        await browser.goto(work.entry_url)
    challenge = 'iframe[src*="captcha"], [class*="altcha"]'
    if await browser.is_visible(challenge):
        _human_barrier = True
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
    field = "#busquedaRucId"
    search_mode = ("Seleccionar búsqueda por RUC o cédula" if work.document_id == 3
                   else "Seleccionar búsqueda por RUC")
    if await browser.count(f'button:has-text("{search_mode}")') == 1:
        await browser.click_text(search_mode, exact=True)
    if await browser.count(field) != 1:
        return {"kind": "RETRYABLE", "reason_code": "EXPECTED_FIELD_NOT_UNIQUE"}
    await browser.fill(field, "")
    await browser.click(field)
    await browser.type_text(field, work.subject.identification)
    if await browser.input_value(field) != work.subject.identification:
        return {"kind": "RETRYABLE", "reason_code": "INPUT_NOT_PERSISTED"}
    if await browser.is_visible(challenge):
        _human_barrier = True
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE",
                "reason_code": "PORTAL_CHALLENGE"}
    button = 'button:has-text("Consultar")'
    enable_deadline = time.monotonic() + min(work.deadline_seconds, 30)
    while time.monotonic() < enable_deadline:
        if await browser.enabled(button):
            break
        await asyncio.sleep(0.5)
    if not await browser.enabled(button):
        return {"kind": "RETRYABLE", "reason_code": "QUERY_NOT_ENABLED"}
    await browser.click_role("button", "Consultar", exact=True)
    deadline = time.monotonic() + min(work.deadline_seconds, 120)
    while time.monotonic() < deadline:
        if await browser.is_visible(challenge):
            _human_barrier = True
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


async def prepare(_work, _services):
    """Reset the challenge latch once per installed sidecar batch."""
    global _human_barrier
    _human_barrier = False


DOCUMENT_FUNCTIONS = {"documento_3": documento_3, "documento_53": documento_53}


async def execute_document(work, services):
    function = DOCUMENT_FUNCTIONS.get(f"documento_{work.document_id}")
    if function is None:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    return await function(work, services)

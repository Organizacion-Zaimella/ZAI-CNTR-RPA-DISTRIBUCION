"""SRI, documentos 3/53. Prototipo privado sujeto a verificación visual TEST."""
from __future__ import annotations

import asyncio
from pathlib import Path
import re
import time
import unicodedata
from urllib.parse import urlparse

SRI_HOST = "srienlinea.sri.gob.ec"
DOCUMENT_ROUTES = {
    3: "/sri-en-linea/SriDeclaracionesWeb/EstadoTributario/Consultas/consultaEstadoTributario",
    53: "/sri-en-linea/SriRucWeb/ConsultaRuc/Consultas/consultaRuc",
}
_human_barrier = False
RESULT_TIMEOUT_SECONDS = 120.0
RESULT_STABILITY_SECONDS = 0.25


def _normalize(text: str) -> str:
    folded = unicodedata.normalize("NFKD", text.casefold())
    return "".join(char for char in folded if not unicodedata.combining(char))


def _classify(document_id: int, visible_text: str, identification: str,
              baseline_text: str = "") -> str | None:
    """Classify a visible result transition and bind matches to the queried RUC."""
    normalized = _normalize(visible_text)
    baseline = _normalize(baseline_text)
    no_match = re.search(r"no se encontraron resultados|no existen resultados", normalized)
    if no_match and no_match.group(0) not in baseline:
        return "NO_MATCH"
    marker = "al dia en sus obligaciones" if document_id == 3 else "activo"
    if marker not in normalized or marker in baseline:
        return None
    digits = re.sub(r"\D", "", identification)
    if 10 <= len(digits) <= 13:
        token = rf"(?<!\d)\d(?:[\s.-]?\d){{{len(digits) - 1}}}(?!\d)"
        if any(re.sub(r"\D", "", item) == digits
               for item in re.findall(token, visible_text)):
            return "MATCH"
    return "MATCH_NOT_ATTRIBUTED"


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
        # The installed 1.0.0 ABI supports this option even before the
        # convenience goto_commit method was added. SRI's Angular app can
        # keep DOMContentLoaded pending; wait only for the response commit.
        await browser.goto(work.entry_url, wait_until="commit")
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
    baseline_text = await browser.text("main")
    await browser.click_role("button", "Consultar", exact=True)
    deadline = time.monotonic() + min(work.deadline_seconds, RESULT_TIMEOUT_SECONDS)
    stable_status = None
    stable_since = None
    unattributed_positive = False
    while time.monotonic() < deadline:
        if await browser.is_visible(challenge):
            _human_barrier = True
            return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
        main = await browser.text("main")
        normalized = _normalize(main)
        if re.search(r"espere por favor|\bcargando\b|\bprocesando\b", normalized):
            stable_status = None
            stable_since = None
            await asyncio.sleep(0.5)
            continue
        kind = _classify(work.document_id, main, work.subject.identification, baseline_text)
        if kind == "MATCH_NOT_ATTRIBUTED":
            unattributed_positive = True
            kind = None
        if kind in {"MATCH", "NO_MATCH"}:
            if kind != stable_status:
                stable_status = kind
                stable_since = time.monotonic()
            elif time.monotonic() - stable_since >= RESULT_STABILITY_SECONDS:
                target = Path(services["evidence_root"]) / f"sri-{work.document_id}-{work.detail_id}.png"
                await browser.screenshot(str(target), full_page=True)
                return {"kind": kind, "evidence_path": str(target)}
        else:
            stable_status = None
            stable_since = None
        await asyncio.sleep(0.25)
    reason = "MATCH_NOT_ATTRIBUTED" if unattributed_positive else "RESULT_NOT_CONCLUSIVE"
    return {"kind": "RETRYABLE", "reason_code": reason}


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

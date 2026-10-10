"""Consejo de la Judicatura, consulta histórica de documentos 73–76.

La URL y los datos de consulta proceden de ORDS. Este módulo no resuelve
reCAPTCHA: devuelve HUMAN_REQUIRED si el portal presenta un reto visible.
"""
from __future__ import annotations

import asyncio
from pathlib import Path
import re
from urllib.parse import urlsplit

from playwright.async_api import TimeoutError as PlaywrightTimeoutError


FIELDS = {
    73: ('[id="form1:txtActorCedula"]', "identification"),
    74: ('[id="form1:txtDemandadoCedula"]', "identification"),
    75: ('[id="form1:txtActor"]', "display_name"),
    76: ('[id="form1:txtDemandadoApellido"]', "display_name"),
}
SEARCH = '[id="form1:butBuscarJuicios"]'
CHALLENGE = 'iframe[src*="recaptcha/api2/bframe"]'
ROWS = 'table:has(th:has-text("No. proceso")) tbody tr:has(td:nth-child(4))'
NO_MATCH = re.compile(r"no se (?:encuentran|encontraron) (?:resultados|registros|coincidencias)", re.I)
DATE = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")
_human_barrier = False


def _safe_entry(url: str) -> str:
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.hostname != "consultas.funcionjudicial.gob.ec"
            or parsed.path != "/informacionjudicial/public/informacion.jsf"
            or parsed.username or parsed.password):
        raise ValueError("URL de entrada judicial no autorizada")
    return url


async def _state(browser) -> str | None:
    global _human_barrier
    if await browser.is_visible(CHALLENGE):
        _human_barrier = True
        return "HUMAN_REQUIRED"
    count = await browser.count(ROWS)
    if count:
        first = await browser.text(f"{ROWS} >> nth=0")
        if DATE.search(first):
            return "MATCH"
    body = await browser.text("body")
    if NO_MATCH.search(body):
        return "NO_MATCH"
    return None


async def _search_idle(browser) -> bool:
    """Detectar cola JSF inactiva antes de la única recuperación histórica."""
    check = getattr(browser, "search_idle", None)
    if check is None:
        return False
    return bool(await check())


async def prepare(_work, _services):
    """Reset the portal barrier once for a new sidecar batch/session."""
    global _human_barrier
    _human_barrier = False


async def _execute_document(work, services, expected_document_id):
    """Ejecutar un único documento; el sidecar administra navegador y evidencia."""
    if work.portal_id != 6 or work.document_id != expected_document_id:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    if _human_barrier:
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "JUDICIAL_SEARCH",
                "reason_code": "PORTAL_CHALLENGE"}
    field, source = FIELDS[work.document_id]
    value = getattr(work.subject, source, None)
    if not isinstance(value, str) or not value.strip():
        return {"kind": "ERROR", "reason_code": "SUBJECT_INPUT_MISSING"}
    try:
        entry = _safe_entry(work.entry_url)
    except ValueError:
        return {"kind": "ERROR", "reason_code": "ENTRY_URL_INVALID"}
    browser = services["browser"]
    try:
        if await browser.is_visible(CHALLENGE):
            await _state(browser)
            return {"kind": "HUMAN_REQUIRED", "checkpoint": "JUDICIAL_SEARCH",
                    "reason_code": "PORTAL_CHALLENGE"}
        await browser.goto(entry, timeout=45000)
        await browser.wait_for_selector(field, state="visible", timeout=15000)
        await browser.fill(field, value.strip())
        if await browser.input_value(field) != value.strip():
            return {"kind": "RETRYABLE", "reason_code": "INPUT_NOT_PERSISTED"}
        if await browser.is_visible(CHALLENGE):
            await _state(browser)  # Fijar la barrera para los demás documentos del lote.
            return {"kind": "HUMAN_REQUIRED", "checkpoint": "JUDICIAL_SEARCH",
                    "reason_code": "RECAPTCHA_VISIBLE"}
        await browser.click(SEARCH)
        loop = asyncio.get_running_loop()
        deadline = loop.time() + min(work.deadline_seconds, 60)
        first_click = loop.time()
        recovery_click_used = False
        while loop.time() < deadline:
            state = await _state(browser)
            if state == "HUMAN_REQUIRED":
                return {"kind": state, "checkpoint": "JUDICIAL_SEARCH", "reason_code": "RECAPTCHA_VISIBLE"}
            if state in ("MATCH", "NO_MATCH"):
                root = Path(services["evidence_root"])
                path = root / f"judicial-{work.execution_id}-{work.detail_id}.png"
                await browser.screenshot(str(path), full_page=True)
                return {"kind": state, "evidence_path": str(path),
                        "recovery_click_used": recovery_click_used}
            if (not recovery_click_used and loop.time() - first_click >= 3
                    and await _search_idle(browser)
                    and await browser.input_value(field) == value.strip()):
                # Historialmente JSF/PrimeFaces podía dejar el formulario
                # intacto aunque el primer click no hubiera iniciado la cola.
                # Recuperar una sola vez solo si el dato sigue intacto y la
                # cola está vacía; nunca duplicar una búsqueda ya en curso.
                await browser.click(SEARCH)
                recovery_click_used = True
            await asyncio.sleep(.5)
        return {"kind": "RETRYABLE", "reason_code": "RESULT_UNVERIFIED",
                "recovery_click_used": recovery_click_used}
    except PlaywrightTimeoutError:
        # El sidecar conserva el navegador abierto; el motor confirma el intento
        # como reintentable y continúa con el siguiente detalle de ORDS.
        return {"kind": "RETRYABLE", "reason_code": "PORTAL_TIMEOUT"}
    except Exception:
        return {"kind": "RETRYABLE", "reason_code": "PORTAL_INTERACTION_FAILED"}


async def documento_73(work, services):
    return await _execute_document(work, services, 73)


async def documento_74(work, services):
    return await _execute_document(work, services, 74)


async def documento_75(work, services):
    return await _execute_document(work, services, 75)


async def documento_76(work, services):
    return await _execute_document(work, services, 76)


DOCUMENT_FUNCTIONS = {
    "documento_73": documento_73, "documento_74": documento_74,
    "documento_75": documento_75, "documento_76": documento_76,
}


async def execute_document(work, services):
    """Compatibilidad para pruebas históricas; el sidecar usa DOCUMENT_FUNCTIONS."""
    function = DOCUMENT_FUNCTIONS.get(f"documento_{work.document_id}")
    if function is None:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    return await function(work, services)

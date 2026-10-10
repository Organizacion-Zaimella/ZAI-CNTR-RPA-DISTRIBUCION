"""Superintendencia 13–19: port privado del handler 2491999.

Solo se ejecuta dentro del sidecar 1.0.0. PortalActions es dueño de Page,
aplica >=5 s a cada acción y provee adquisición PDF genérica autenticada.
No reanuda ni resuelve ALTCHA; deja checkpoint para una etapa atendida.
"""
from __future__ import annotations

import asyncio
from pathlib import Path
import re
import time
from urllib.parse import urlsplit

from playwright.async_api import TimeoutError as PlaywrightTimeoutError


DOCUMENTS = frozenset(range(13, 20))
PORTAL_ID = 1
EXPECTED_HOST = "appscvsgen.supercias.gob.ec"
_subject_id = None
_human_barrier = False


class HumanBarrier(Exception):
    def __init__(self, phase):
        self.phase = phase


class StateFault(Exception):
    def __init__(self, code):
        self.code = code


async def prepare(_work, _services):
    global _subject_id, _human_barrier
    _subject_id = None
    _human_barrier = False


async def _barrier(browser):
    global _human_barrier
    if _human_barrier:
        return True
    selector = 'altcha-widget:not([state="verified"])'
    count = await browser.count(selector)
    if count > 1:
        _human_barrier = True
        return True
    blocked = count == 1 and await browser.is_visible(selector)
    if blocked:
        _human_barrier = True
    return blocked


async def _wait(browser, predicate, deadline, phase):
    while time.monotonic() < deadline:
        if await _barrier(browser):
            raise HumanBarrier(phase)
        if await predicate():
            return
        await asyncio.sleep(0.25)
    raise StateFault("PORTAL_POSTCONDITION_TIMEOUT")


async def _action(browser, method, phase, *args):
    if await _barrier(browser):
        raise HumanBarrier(phase)
    result = await getattr(browser, method)(*args)
    if await _barrier(browser):
        raise HumanBarrier(phase)
    return result


async def _record_ready(browser, work):
    # La mera presencia del RUC en el textbox no acredita la ficha.
    if not await browser.is_visible('a:has-text("Consulta de cumplimiento")'):
        return False
    return work.subject.display_name.casefold() in (await browser.text("body")).casefold()


async def _ensure_subject(work, browser, deadline):
    global _subject_id
    if _subject_id == work.subject.id and await _record_ready(browser, work):
        return
    if _subject_id not in (None, work.subject.id):
        raise StateFault("SESSION_SUBJECT_MISMATCH")
    await _action(browser, "goto", "entry", work.entry_url)
    radio_label = 'label[for="frmBusquedaCompanias:tipoBusqueda:1"]'
    await _wait(browser, lambda: browser.is_visible(radio_label), deadline, "ruc_radio")
    await _action(browser, "click", "ruc_radio", radio_label)
    radio = 'input[id="frmBusquedaCompanias:tipoBusqueda:1"]'
    if not await browser.is_checked(radio):
        raise StateFault("RUC_RADIO_NOT_SELECTED")
    field = 'input[id="frmBusquedaCompanias:parametroBusqueda_input"]'
    await _wait(browser, lambda: browser.is_visible(field), deadline, "ruc_field")
    await _action(browser, "fill", "ruc_clear", field, "")
    # T05 type_text pasa cada tecla por PortalPacer; la sugerencia JSF requiere
    # eventos de teclado y el handler histórico demostró que fill solo no basta.
    await _action(browser, "type_text", "ruc_keyboard", field, work.subject.identification)
    suggestion = 'li.ui-autocomplete-item'
    await _wait(browser, lambda: browser.count(suggestion), deadline, "company_suggestion")
    if await browser.count(suggestion) != 1:
        raise StateFault("COMPANY_SUGGESTION_AMBIGUOUS")
    if work.subject.identification not in await browser.text(suggestion):
        raise StateFault("COMPANY_SUGGESTION_MISMATCH")
    await _action(browser, "click", "company_suggestion", suggestion)
    if not await _record_ready(browser, work):
        await _wait(browser,
                    lambda: browser.is_visible('button:has-text("Consultar")'),
                    deadline, "consult_button")
        await _action(browser, "click_role", "consult_company", "button", "Consultar")
        await _wait(browser, lambda: _record_ready(browser, work), deadline, "subject_record")
    _subject_id = work.subject.id


async def _open_menu(browser, work, name, ready, deadline):
    if not await _record_ready(browser, work):
        raise StateFault("SUBJECT_RECORD_LOST")
    if await ready():
        return
    await _action(browser, "click_role", "open_menu", "link", name)
    await _wait(browser, ready, deadline, "document_section")


async def _dialog_pdf(browser, work, title_pattern, deadline, evidence_root):
    dialog = '.ui-dialog:visible'
    while time.monotonic() < deadline:
        if await _barrier(browser):
            raise HumanBarrier("pdf_dialog")
        if await browser.count(dialog) == 1:
            title = await browser.text(dialog + ' .ui-dialog-title')
            if re.search(title_pattern, title, re.I):
                break
        if await browser.is_visible('button:has-text("Continuar")'):
            await _action(browser, "click_role", "continue_to_pdf", "button", "Continuar")
        await asyncio.sleep(0.25)
    else:
        raise StateFault("PDF_DIALOG_NOT_READY")
    target = Path(evidence_root) / f"supercias-{work.document_id}-{work.detail_id}.pdf"
    # Método genérico T05: solo URL same-origin object/embed/iframe, respuesta
    # application/pdf sin redirect y validación estructural antes de retornar.
    while time.monotonic() < deadline:
        if await _barrier(browser):
            raise HumanBarrier("pdf_dialog")
        try:
            await browser.save_same_origin_pdf_from_dialog(dialog, str(target))
            break
        except Exception:
            # El object PDF temporal puede preceder a los bytes completos.
            # Releer la URL del visor; nunca repetir el botón de negocio.
            await asyncio.sleep(0.25)
    else:
        raise StateFault("PDF_NOT_VALID_IN_DIALOG")
    await _action(browser, "click", "close_pdf_dialog",
                  dialog + ' .ui-dialog-titlebar-close')
    await _wait(browser, lambda: _hidden(browser, dialog), deadline, "dialog_hidden")
    if not await _record_ready(browser, work):
        raise StateFault("SUBJECT_RECORD_LOST_AFTER_PDF")
    return target


async def _hidden(browser, selector):
    return not await browser.is_visible(selector)


async def _simple_document(browser, work, deadline, evidence_root):
    paths = {
        13: ("Consulta de cumplimiento", "Generar certificado", "CUMPLIMIENTO DE OBLIGACIONES"),
        14: ("Beneficiario final de accionistas/socios", "Exportar a PDF", "BENEFICIARIOS FINALES"),
        15: ("Información general", "Imprimir certificado", "INFORMACIÓN GENERAL"),
    }
    menu, button, title = paths[work.document_id]
    ready = lambda: browser.is_visible(f'button:has-text("{button}")')
    await _open_menu(browser, work, menu, ready, deadline)
    await _action(browser, "click_role", "export_document", "button", button)
    return await _dialog_pdf(browser, work, title, deadline, evidence_root)


async def _incorporation(browser, work, deadline, evidence_root):
    await _open_menu(browser, work, "Documentos online",
                     lambda: browser.is_visible('text=DOCUMENTACIÓN DE LA COMPAÑÍA'), deadline)
    row = 'tr:has-text("CONSTITUCIÓN"):has-text("Escritura")'
    if await browser.count(row) != 1:
        await _action(browser, "click_role", "legal_tab", "tab", "Documentos jurídicos")
        await _wait(browser, lambda: browser.count(row), deadline, "incorporation_row")
    if await browser.count(row) != 1:
        raise StateFault("INCORPORATION_ROW_AMBIGUOUS")
    link = row + ' a:has(img[alt*="PDF" i])'
    if await browser.count(link) != 1:
        raise StateFault("INCORPORATION_PDF_LINK_AMBIGUOUS")
    await _action(browser, "click", "open_incorporation_pdf", link)
    return await _dialog_pdf(browser, work, r"ESCRITURA.*CONSTITUCIÓN", deadline, evidence_root)


async def _document_column(browser, table, title):
    data_id = await browser.attribute(table, "id")
    if not data_id or not data_id.endswith("_data") or not re.fullmatch(r"[\w:-]+", data_id):
        raise StateFault("DOCUMENT_TABLE_ID_INVALID")
    prefix = data_id[:-5]
    header = f'th[id^="{prefix}:"]:has-text("{title}")'
    if await browser.count(header) != 1:
        raise StateFault("DOCUMENT_COLUMN_AMBIGUOUS")
    return header


async def _latest_row(browser, table, title, manager, deadline):
    document_header = await _document_column(browser, table, "Documento")
    document_filter = document_header + ' input[id$=":filter"]'
    await _action(browser, "fill", "document_filter", document_filter, title)
    await _action(browser, "press", "document_filter_enter", document_filter, "Enter")
    if manager:
        cargo_header = await _document_column(browser, table, "Cargo")
        cargo_filter = cargo_header + ' input[id$=":filter"]'
        await _action(browser, "fill", "cargo_filter", cargo_filter, manager)
        await _action(browser, "press", "cargo_filter_enter", cargo_filter, "Enter")
    row = table + ' tr:has(td)'
    await _wait(browser, lambda: browser.count(row), deadline, "filtered_rows")
    date_header = await _document_column(browser, table, "Fecha")
    for _ in range(2):
        if (await browser.attribute(date_header, "aria-sort") or "").lower() == "descending":
            break
        previous = (await browser.attribute(date_header, "aria-sort") or "").lower()
        await _action(browser, "click", "sort_date", date_header + ' .ui-column-title')
        await _wait(browser, lambda: _sort_changed(browser, date_header, previous),
                    deadline, "date_sort")
    if not await _sorted(browser, date_header):
        raise StateFault("DATE_NOT_DESCENDING")
    if await browser.count(row) < 1:
        raise StateFault("FILTERED_ROW_ABSENT")
    first = row + ':first-child'
    first_text = await browser.text(first)
    if title.casefold() not in first_text.casefold() or (manager and manager.casefold() not in first_text.casefold()):
        raise StateFault("FILTERED_ROW_MISMATCH")
    date = (await browser.text(first + ' td:nth-child(2)')).strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise StateFault("LATEST_DATE_INVALID")
    if await browser.count(row) > 1:
        second_date = (await browser.text(row + ':nth-child(2) td:nth-child(2)')).strip()
        if second_date == date:
            raise StateFault("LATEST_DATE_TIED")
    return first


async def _sorted(browser, header):
    return (await browser.attribute(header, "aria-sort") or "").lower() == "descending"


async def _sort_changed(browser, header, previous):
    return (await browser.attribute(header, "aria-sort") or "").lower() != previous


async def _table_document(browser, work, deadline, evidence_root):
    await _open_menu(browser, work, "Documentos online",
                     lambda: browser.is_visible('text=DOCUMENTACIÓN DE LA COMPAÑÍA'), deadline)
    if work.document_id == 16:
        tab, table, label, title, manager = (
            "Documentos generales", '[id$="tblDocumentosGenerales_data"]',
            "Nombramiento", "NOMBRAMIENTO", "GERENTE GENERAL")
    else:
        tab, table, label, title, manager = (
            "Documentos económicos", '[id$="tblDocumentosEconomicos_data"]',
            "Estado de Resultado Integral" if work.document_id == 18 else
            "Balance / Estado de Situación Financiera",
            "RESULTADO INTEGRAL" if work.document_id == 18 else
            r"BALANCE|SITUACI[ÓO]N FINANCIERA", None)
    if not await browser.is_visible(table):
        await _action(browser, "click_role", "document_tab", "tab", tab)
        await _wait(browser, lambda: browser.is_visible(table), deadline, "document_table")
    row = await _latest_row(browser, table, label, manager, deadline)
    link = row + ' a:has(img[alt*="PDF" i])'
    if await browser.count(link) != 1:
        raise StateFault("LATEST_PDF_LINK_AMBIGUOUS")
    await _action(browser, "click", "open_latest_pdf", link)
    return await _dialog_pdf(browser, work, title, deadline, evidence_root)


async def _execute_document(work, services, expected_document_id):
    if _human_barrier:
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "SUPERCIAS_PORTAL_CHALLENGE",
                "reason_code": "PORTAL_CHALLENGE"}
    if work.portal_id != PORTAL_ID or work.document_id != expected_document_id:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    entry = urlsplit(work.entry_url)
    if entry.scheme != "https" or entry.hostname != EXPECTED_HOST:
        return {"kind": "ERROR", "reason_code": "UNAPPROVED_PORTAL_ORIGIN"}
    if work.subject.type.value != "EMPRESA":
        return {"kind": "ERROR", "reason_code": "SUBJECT_TYPE_UNSUPPORTED"}
    browser = services["browser"]
    deadline = time.monotonic() + work.deadline_seconds
    try:
        await _ensure_subject(work, browser, deadline)
        if work.document_id in (13, 14, 15):
            target = await _simple_document(browser, work, deadline, services["evidence_root"])
        elif work.document_id == 17:
            target = await _incorporation(browser, work, deadline, services["evidence_root"])
        else:
            target = await _table_document(browser, work, deadline, services["evidence_root"])
        return {"kind": "MATCH", "evidence_path": str(target)}
    except HumanBarrier as barrier:
        return {"kind": "HUMAN_REQUIRED", "checkpoint": f"SUPERCIAS_{barrier.phase.upper()}"}
    except StateFault as fault:
        return {"kind": "RETRYABLE", "reason_code": fault.code}
    except (PlaywrightTimeoutError, TimeoutError):
        return {"kind": "RETRYABLE", "reason_code": "PORTAL_TIMEOUT"}
    except Exception:
        # Sin datos de sujeto ni detalles de respuesta en IPC/log público.
        return {"kind": "RETRYABLE", "reason_code": "PORTAL_ADAPTER_FAILURE"}


async def documento_13(work, services):
    return await _execute_document(work, services, 13)


async def documento_14(work, services):
    return await _execute_document(work, services, 14)


async def documento_15(work, services):
    return await _execute_document(work, services, 15)


async def documento_16(work, services):
    return await _execute_document(work, services, 16)


async def documento_17(work, services):
    return await _execute_document(work, services, 17)


async def documento_18(work, services):
    return await _execute_document(work, services, 18)


async def documento_19(work, services):
    return await _execute_document(work, services, 19)


DOCUMENT_FUNCTIONS = {
    "documento_13": documento_13, "documento_14": documento_14,
    "documento_15": documento_15, "documento_16": documento_16,
    "documento_17": documento_17, "documento_18": documento_18,
    "documento_19": documento_19,
}


async def execute_document(work, services):
    """Compatibilidad para pruebas históricas; el sidecar usa DOCUMENT_FUNCTIONS."""
    function = DOCUMENT_FUNCTIONS.get(f"documento_{work.document_id}")
    if function is None:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    return await function(work, services)

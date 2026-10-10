"""SERCOP, documento 11; selector y ramas del workflow ACTIVO 70/v3 TEST."""
from __future__ import annotations

import asyncio
from pathlib import Path
import time
import unicodedata


def _fold(value: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", value.casefold())
                   if not unicodedata.combining(c))


async def documento_11(work, services):
    if work.portal_id != 11 or work.document_id != 11:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    browser = services["browser"]
    await browser.goto(work.entry_url)
    if await browser.is_visible('iframe[src*="captcha"], [class*="altcha"]'):
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
    await browser.fill_role("textbox", "", work.subject.identification)
    await browser.click_role("button", "Buscar Proveedor")
    deadline = time.monotonic() + min(work.deadline_seconds, 120)
    while time.monotonic() < deadline:
        if await browser.is_visible('iframe[src*="captcha"], [class*="altcha"]'):
            return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
        body = _fold(await browser.text("body"))
        if "no se encontro resultados con este criterio de busqueda" in body:
            kind = "NO_MATCH"
        elif "proveedores incumplidos y adjudicatarios fallidos reportados al sercop" in body:
            # Encabezado de página; no prueba una fila positiva atribuida.
            return {"kind": "RETRYABLE", "reason_code": "MATCH_NOT_ATTRIBUTED"}
        else:
            await asyncio.sleep(0.5)
            continue
        target = Path(services["evidence_root"]) / f"sercop-{work.detail_id}.png"
        await browser.screenshot(str(target), full_page=True)
        return {"kind": kind, "evidence_path": str(target)}
    return {"kind": "RETRYABLE", "reason_code": "RESULT_NOT_CONCLUSIVE"}


DOCUMENT_FUNCTIONS = {"documento_11": documento_11}


async def execute_document(work, services):
    return await documento_11(work, services)

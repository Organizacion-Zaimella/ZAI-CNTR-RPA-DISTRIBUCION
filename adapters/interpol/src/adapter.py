"""INTERPOL, documento 12. Nombres separados; nunca usar identificación en Apellidos."""
from __future__ import annotations

import asyncio
from pathlib import Path
import time


async def documento_12(work, services):
    if work.portal_id != 12 or work.document_id != 12:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    if not work.subject.surnames or not work.subject.names:
        return {"kind": "ERROR", "reason_code": "SUBJECT_NAMES_REQUIRED"}
    browser = services["browser"]
    await browser.goto(work.entry_url)
    if await browser.is_visible('iframe[src*="captcha"], [class*="altcha"]'):
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
    await browser.fill_label("Apellidos", work.subject.surnames)
    await browser.fill_label("Nombre", work.subject.names)
    await browser.click_role("button", "Buscar")
    deadline = time.monotonic() + min(work.deadline_seconds, 120)
    while time.monotonic() < deadline:
        if await browser.is_visible('iframe[src*="captcha"], [class*="altcha"]'):
            return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
        body = (await browser.text("body")).casefold()
        if "no hay resultados para su búsqueda. seleccione otros criterios." in body:
            kind = "NO_MATCH"
        elif "resultados de la búsqueda:" in body:
            # Encabezado genérico; exige una coincidencia individual verificable.
            return {"kind": "RETRYABLE", "reason_code": "MATCH_NOT_ATTRIBUTED"}
        else:
            await asyncio.sleep(0.5)
            continue
        target = Path(services["evidence_root"]) / f"interpol-{work.detail_id}.png"
        await browser.screenshot(str(target), full_page=True)
        return {"kind": kind, "evidence_path": str(target)}
    return {"kind": "RETRYABLE", "reason_code": "RESULT_NOT_CONCLUSIVE"}


DOCUMENT_FUNCTIONS = {"documento_12": documento_12}


async def execute_document(work, services):
    return await documento_12(work, services)

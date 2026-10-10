"""OFAC, documento 5. Prototipo privado; requiere certificación TEST 1.0.0."""
from __future__ import annotations

import asyncio
from pathlib import Path
import re
import time


PORTAL_ID = 5
DOCUMENT_IDS = {5}
RESULT = re.compile(r"Lookup Results:\s*(\d+)\s*Found", re.I)


async def documento_5(work, services):
    if work.portal_id != PORTAL_ID or work.document_id != 5:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    browser = services["browser"]
    await browser.goto(work.entry_url)
    if await browser.is_visible('iframe[src*="captcha"], [class*="altcha"]'):
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
    await browser.fill_role("textbox", "Enter name as search criteria.", work.subject.display_name)
    await browser.click_role("button", "Search")
    deadline = time.monotonic() + min(work.deadline_seconds, 120)
    while time.monotonic() < deadline:
        if await browser.is_visible('iframe[src*="captcha"], [class*="altcha"]'):
            return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
        found = RESULT.search(await browser.text("body"))
        if found:
            target = Path(services["evidence_root"]) / f"ofac-{work.detail_id}.png"
            await browser.screenshot(str(target), full_page=True)
            return {"kind": "MATCH" if int(found.group(1)) > 0 else "NO_MATCH",
                    "evidence_path": str(target)}
        await asyncio.sleep(0.5)
    return {"kind": "RETRYABLE", "reason_code": "RESULT_NOT_CONCLUSIVE"}


DOCUMENT_FUNCTIONS = {"documento_5": documento_5}


async def execute_document(work, services):
    return await documento_5(work, services)

"""OFAC, documento 5. Prototipo privado; requiere certificación TEST 1.0.0."""
from __future__ import annotations

import asyncio
from pathlib import Path
import re
import time
from urllib.parse import urlparse


PORTAL_ID = 5
DOCUMENT_IDS = {5}
RESULT = re.compile(r"Lookup Results:\s*(\d+)\s*Found", re.I)
PORTAL_BUSY = re.compile(r"please wait|searching|loading|espere por favor|\bcargando\b", re.I)
RESULT_STABLE_SAMPLES = 2
OFAC_HOST = "sanctionssearch.ofac.treas.gov"
_human_barrier = False


def _failure_code(exc: Exception) -> str:
    message = str(exc).upper()
    markers = (
        ("ERR_INTERNET_DISCONNECTED", "NETWORK_DISCONNECTED"),
        ("ERR_NETWORK_CHANGED", "NETWORK_CHANGED"),
        ("ERR_CONNECTION_RESET", "PORTAL_CONNECTION_RESET"),
        ("ERR_CONNECTION_REFUSED", "PORTAL_CONNECTION_REFUSED"),
        ("ERR_NAME_NOT_RESOLVED", "PORTAL_DNS_FAILURE"),
        ("ERR_CONNECTION_TIMED_OUT", "PORTAL_CONNECTION_TIMEOUT"),
        ("ERR_TIMED_OUT", "PORTAL_CONNECTION_TIMEOUT"),
        ("ERR_ADDRESS_UNREACHABLE", "PORTAL_UNREACHABLE"),
    )
    if type(exc).__name__.casefold() == "timeouterror":
        return "PORTAL_TIMEOUT"
    return next((reason for marker, reason in markers if marker in message),
                "PORTAL_ACTION_FAILED")


async def documento_5(work, services):
    global _human_barrier
    if work.portal_id != PORTAL_ID or work.document_id != 5:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    if _human_barrier:
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE",
                "reason_code": "PORTAL_CHALLENGE"}
    parsed = urlparse(work.entry_url)
    if parsed.scheme != "https" or parsed.hostname != OFAC_HOST:
        return {"kind": "ERROR", "reason_code": "UNAUTHORIZED_ENTRY_URL"}
    browser = services["browser"]
    try:
        response = await browser.goto(work.entry_url)
        if response is not None and getattr(response, "status", None) in (403, 429, 451):
            return {"kind": "RETRYABLE", "reason_code": f"PORTAL_HTTP_{response.status}"}
        if await browser.is_visible('iframe[src*="captcha"], [class*="altcha"]'):
            _human_barrier = True
            return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE",
                    "reason_code": "PORTAL_CHALLENGE"}
        await browser.fill_role("textbox", "Enter name as search criteria.",
                                work.subject.display_name, exact=True)
        await browser.click_role("button", "Search", exact=True)
        deadline = time.monotonic() + min(work.deadline_seconds, 120)
        stable_count = None
        stable_samples = 0
        while time.monotonic() < deadline:
            if await browser.is_visible('iframe[src*="captcha"], [class*="altcha"]'):
                _human_barrier = True
                return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE",
                        "reason_code": "PORTAL_CHALLENGE"}
            text = await browser.text("body")
            if PORTAL_BUSY.search(text):
                stable_count = None
                stable_samples = 0
                await asyncio.sleep(0.5)
                continue
            found = RESULT.search(text)
            if found:
                observed = int(found.group(1))
                if observed == stable_count:
                    stable_samples += 1
                else:
                    stable_count = observed
                    stable_samples = 1
                if stable_samples >= RESULT_STABLE_SAMPLES:
                    target = Path(services["evidence_root"]) / f"ofac-{work.detail_id}.png"
                    await browser.screenshot(str(target), full_page=True)
                    return {"kind": "MATCH" if observed else "NO_MATCH",
                            "evidence_path": str(target)}
            else:
                stable_count = None
                stable_samples = 0
            await asyncio.sleep(0.5)
        return {"kind": "RETRYABLE", "reason_code": "RESULT_NOT_CONCLUSIVE"}
    except Exception as exc:
        return {"kind": "RETRYABLE", "reason_code": _failure_code(exc)}


DOCUMENT_FUNCTIONS = {"documento_5": documento_5}


async def execute_document(work, services):
    return await documento_5(work, services)


async def prepare(_work, _services):
    global _human_barrier
    _human_barrier = False

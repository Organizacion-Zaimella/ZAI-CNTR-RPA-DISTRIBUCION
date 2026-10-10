"""IESS documento 2: consulta pública y validación de PDF nativo para el sidecar."""
from __future__ import annotations

from pathlib import Path
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

MAX_PDF_BYTES = 25 * 1024 * 1024


def classify_portal_error(exc: Exception) -> str:
    """Return a bounded technical code; never persist exception text or URLs."""
    if isinstance(exc, (TimeoutError, PlaywrightTimeoutError)):
        return "PORTAL_TIMEOUT"
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
    return next((code for marker, code in markers if marker in message),
                "PORTAL_ACTION_FAILED")


def valid_pdf_for_ords(path: Path) -> bool:
    """Asegurar los marcadores PDF mínimos antes de entregar evidencia al motor."""
    try:
        size = path.stat().st_size
        if not path.is_file() or not 100 < size <= MAX_PDF_BYTES:
            return False
        with path.open("rb") as source:
            header = source.read(5)
            source.seek(max(0, size - 8192))
            trailer = source.read(8192)
            source.seek(0)
            contains_xref = b"startxref" in source.read(MAX_PDF_BYTES + 1)
        return header == b"%PDF-" and contains_xref and b"%%EOF" in trailer
    except OSError:
        return False


async def documento_2(work, services):
    """Consultar el documento IESS 2 usando únicamente la fachada del sidecar."""
    if work.portal_id != 2 or work.document_id != 2:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}

    browser = services["browser"]
    target = Path(services["evidence_root"]) / f"iess-{work.detail_id}.pdf"
    try:
        await browser.goto(work.entry_url)
        if await browser.is_visible('iframe[src*="captcha"], [class*="altcha"]'):
            return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
        # None leaves the accessible-name filter unset, matching the exact
        # unique textbox check used by the independently tested app.py.
        await browser.fill_role("textbox", None, work.subject.identification)
        # The legacy successful IESS workflow used pdf.acquire, whose first
        # capture strategy is the browser-owned download event. Preserve that
        # behavior through the stable sidecar facade; never click twice to try
        # another transport after a timeout.
        await browser.download_by_click(
            'button:has-text("CONSULTAR")', str(target)
        )
        if not valid_pdf_for_ords(target):
            target.unlink(missing_ok=True)
            return {"kind": "RETRYABLE", "reason_code": "NATIVE_PDF_STRUCTURE_INVALID"}
        return {"kind": "MATCH", "evidence_path": str(target)}
    except Exception as exc:
        target.unlink(missing_ok=True)
        return {"kind": "RETRYABLE", "reason_code": classify_portal_error(exc)}


DOCUMENT_FUNCTIONS = {"documento_2": documento_2}


async def execute_document(work, services):
    """Compatibilidad para invocación directa de la función documental."""
    return await documento_2(work, services)

"""Lista Clinton (Oracle documento 33): búsqueda determinista del PDF SDN."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit

PORTAL_ID = 134
DOCUMENT_ID = 33
ALLOWED_HOST = "www.treasury.gov"
ALLOWED_PATH = "/ofac/downloads/sdnlist.pdf"
MAX_PDF_BYTES = 25 * 1024 * 1024
MAX_PAGES = 10_000


def _network_failure_code(exc: Exception) -> str:
    """Map browser exceptions to bounded codes; never return raw exception data."""
    if type(exc).__name__.casefold() == "timeouterror":
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
                "PORTAL_UNAVAILABLE")


def normalize(value: str) -> str:
    """Normalize typography only; retain every letter and digit for matching."""
    return "".join(char for char in unicodedata.normalize("NFD", value.casefold())
                   if not unicodedata.combining(char) and char.isalnum())


def validate_url(value: str) -> str:
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or parsed.netloc != ALLOWED_HOST or
            parsed.path != ALLOWED_PATH or parsed.username or parsed.password or
            parsed.query or parsed.fragment):
        raise ValueError("URL pública de Lista Clinton no autorizada")
    return value


def search_and_bundle(pdf_bytes: bytes, query: str, evidence_dir: Path,
                      detail_id: int, *, fitz_module=None) -> dict:
    """Search every text page and return an auditable PDF bundle.

    A negative result is conclusive only when all pages contain extractable
    text. The bundle starts with a search receipt and retains the source PDF.
    """
    if not isinstance(pdf_bytes, bytes) or not 5 < len(pdf_bytes) <= MAX_PDF_BYTES:
        return {"status": "RETRYABLE", "reason_code": "PDF_SIZE_INVALID"}
    if not pdf_bytes.startswith(b"%PDF-"):
        return {"status": "RETRYABLE", "reason_code": "PDF_SIGNATURE_INVALID"}
    normalized_query = normalize(query)
    if not normalized_query:
        return {"status": "ERROR", "reason_code": "SUBJECT_NAME_EMPTY"}

    if fitz_module is None:
        import fitz as fitz_module
    target = evidence_dir / f"lista-clinton-{detail_id}.pdf"
    try:
        with fitz_module.open(stream=pdf_bytes, filetype="pdf") as source:
            page_count = source.page_count
            if not 0 < page_count <= MAX_PAGES:
                return {"status": "RETRYABLE", "reason_code": "PDF_PAGE_LIMIT"}
            matches: list[int] = []
            empty_pages: list[int] = []
            for page_number in range(page_count):
                text = normalize(source.load_page(page_number).get_text("text") or "")
                if len(text) > 2_000_000:
                    return {"status": "RETRYABLE", "reason_code": "PDF_PAGE_TEXT_LIMIT"}
                if not text:
                    empty_pages.append(page_number + 1)
                if normalized_query in text:
                    matches.append(page_number + 1)
            if not matches and empty_pages:
                return {"status": "RETRYABLE", "reason_code": "PDF_TEXT_INCOMPLETE",
                        "pages_without_text": len(empty_pages)}
            business_status = "MATCH" if matches else "NO_MATCH"
            digest = hashlib.sha256(pdf_bytes).hexdigest()
            evidence_dir.mkdir(parents=True, exist_ok=True)
            bundle = fitz_module.open()
            cover = bundle.new_page(width=612, height=792)
            result_text = "COINCIDENCIA ENCONTRADA" if matches else "SIN COINCIDENCIAS"
            details = (f"LISTA CLINTON — resultado de búsqueda\n\n"
                       f"Consulta: {query}\n"
                       f"Resultado: {result_text}\n"
                       f"Coincidencias: {len(matches)}\n"
                       f"Páginas coincidentes (primeras 30): "
                       f"{', '.join(map(str, matches[:30])) or 'ninguna'}\n"
                       f"Páginas revisadas: {page_count}\n"
                       f"Páginas sin texto extraíble: {len(empty_pages)}\n"
                       f"SHA-256 del PDF fuente: {digest}\n"
                       f"Evidencia: documento {DOCUMENT_ID}; detalle {detail_id}\n\n"
                       "Método: coincidencia literal normalizada (acentos, espacios y puntuación "
                       "se ignoran); no se usa OCR. El PDF fuente comienza en la página siguiente.")
            cover.insert_textbox((42, 48, 570, 740), details, fontsize=12,
                                 fontname="helv", lineheight=1.35)
            with fitz_module.open(stream=pdf_bytes, filetype="pdf") as source:
                bundle.insert_pdf(source)
            bundle.set_metadata({"title": "Lista Clinton — búsqueda documental",
                                 "subject": "Resultado automatizado y PDF fuente público"})
            bundle.save(target, garbage=4, deflate=True)
            bundle.close()
        if target.stat().st_size > MAX_PDF_BYTES:
            target.unlink(missing_ok=True)
            return {"status": "RETRYABLE", "reason_code": "EVIDENCE_SIZE_LIMIT"}
        return {"status": business_status, "evidence_path": str(target),
                "evidence_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "source_pdf_sha256": digest, "match_count": len(matches),
                "pages_checked": page_count, "matched_pages": matches}
    except Exception:
        target.unlink(missing_ok=True)
        return {"status": "RETRYABLE", "reason_code": "PDF_SEARCH_FAILED"}


def _context(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("portal_id") != PORTAL_ID or raw.get("document_id") != DOCUMENT_ID:
        raise ValueError("documento no soportado")
    url = validate_url(str(raw["entry_url"]))
    query = str(raw.get("display_name", "")).strip()
    if not query or len(query) > 300:
        raise ValueError("contexto incompleto")
    evidence_dir = Path(raw["evidence_dir"]).resolve()
    repo = Path(__file__).resolve().parents[2]
    if path.resolve().is_relative_to(repo) or evidence_dir.is_relative_to(repo):
        raise ValueError("contexto y evidencia deben permanecer fuera del repositorio")
    return {"url": url, "query": query, "evidence_dir": evidence_dir,
            "detail_id": int(raw.get("detail_id", 1)),
            "timeout_seconds": min(3600, max(15, int(raw.get("timeout_seconds", 300))))}


async def _download_pdf(url: str, timeout_seconds: int) -> tuple[bytes | None, str | None]:
    from playwright.async_api import async_playwright

    async with async_playwright() as playwright:
        browser = None
        for channel in ("msedge", "chrome"):
            try:
                browser = await playwright.chromium.launch(channel=channel, headless=True)
                break
            except Exception:
                continue
        if browser is None:
            return None, "NO_SUPPORTED_BROWSER"
        try:
            page = await browser.new_page(accept_downloads=True)
            try:
                response = await page.goto(url, wait_until="commit", timeout=timeout_seconds * 1000)
            except Exception as exc:
                return None, _network_failure_code(exc)
            if response is None:
                return None, "PDF_RESPONSE_MISSING"
            if response.status in (403, 429, 451):
                return None, f"HTTP_{response.status}"
            if response.status != 200:
                return None, "PDF_HTTP_RESPONSE_INVALID"
            body = await response.body()
            if not body.startswith(b"%PDF-"):
                return None, "PDF_SIGNATURE_INVALID"
            return body, None
        finally:
            await browser.close()


async def run(context: dict) -> dict:
    try:
        body, failure = await _download_pdf(context["url"], context["timeout_seconds"])
        if failure:
            status = "BLOCKED" if failure.startswith("HTTP_") else "RETRYABLE"
            return {"adapter_id": "lista-clinton", "adapter_version": "0.1.0-candidate",
                    "status": status, "reason_code": failure}
        result = search_and_bundle(body, context["query"], context["evidence_dir"],
                                   context["detail_id"])
        return {"adapter_id": "lista-clinton", "adapter_version": "0.1.0-candidate",
                **result}
    except Exception:
        return {"adapter_id": "lista-clinton", "adapter_version": "0.1.0-candidate",
                "status": "RETRYABLE", "reason_code": "PORTAL_OR_BROWSER_ERROR"}


async def documento_33(work, services):
    """Sidecar ABI: use the Oracle-assigned name and PDF URL; never order work."""
    if work.portal_id != PORTAL_ID or work.document_id != DOCUMENT_ID:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    try:
        url = validate_url(work.entry_url)
    except ValueError:
        return {"kind": "ERROR", "reason_code": "ENTRY_URL_NOT_ALLOWED"}
    browser = services["browser"]
    try:
        response = await browser.goto(url, wait_until="commit")
        if response is None:
            return {"kind": "RETRYABLE", "reason_code": "PDF_RESPONSE_MISSING"}
        if response.status in (403, 429, 451):
            return {"kind": "RETRYABLE", "reason_code": f"HTTP_{response.status}"}
        if response.status != 200:
            return {"kind": "RETRYABLE", "reason_code": "PDF_HTTP_RESPONSE_INVALID"}
        body = await response.body()
        result = search_and_bundle(body, work.subject.display_name,
                                   Path(services["evidence_root"]), work.detail_id)
        kind = result["status"]
        if kind in {"MATCH", "NO_MATCH"}:
            return {"kind": kind, "evidence_path": result["evidence_path"]}
        return {"kind": "RETRYABLE" if kind == "RETRYABLE" else "ERROR",
                "reason_code": result.get("reason_code", "PDF_SEARCH_FAILED")}
    except Exception as exc:
        return {"kind": "RETRYABLE", "reason_code": _network_failure_code(exc)}


DOCUMENT_FUNCTIONS = {"documento_33": documento_33}


def main() -> int:
    parser = argparse.ArgumentParser(description="Lista Clinton standalone TEST adapter")
    parser.add_argument("--context", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = asyncio.run(run(_context(args.context.resolve())))
    except Exception:
        result = {"adapter_id": "lista-clinton", "adapter_version": "0.1.0-candidate",
                  "status": "ERROR", "reason_code": "INVALID_CONTEXT"}
    print(json.dumps(result, separators=(",", ":"), ensure_ascii=True))
    return 0 if result["status"] in {"MATCH", "NO_MATCH"} else 1


if __name__ == "__main__":
    sys.exit(main())

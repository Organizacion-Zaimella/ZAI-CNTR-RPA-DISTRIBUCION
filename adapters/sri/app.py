"""Standalone Playwright application for SRI documents 3 and 53.

The JSON context is supplied locally by an authorized TEST harness. It must not
be committed: it contains a subject identifier. This module never logs it.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
import sys
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright


ADAPTER_ID = "sri"
ADAPTER_VERSION = "0.1.9-candidate"
MIN_PACING_SECONDS = 5.0
NAVIGATION_TIMEOUT_SECONDS = 45.0
ELEMENT_TIMEOUT_SECONDS = 45.0
RESULT_TIMEOUT_SECONDS = 120.0
DOCUMENT_ROUTES = {
    3: "/sri-en-linea/SriDeclaracionesWeb/EstadoTributario/Consultas/consultaEstadoTributario",
    53: "/sri-en-linea/SriRucWeb/ConsultaRuc/Consultas/consultaRuc",
}
SRI_HOST = "srienlinea.sri.gob.ec"
_human_barrier = False


@dataclass(frozen=True)
class WorkContext:
    document_id: int
    entry_url: str
    identification: str
    evidence_dir: Path
    pacing_seconds: float = MIN_PACING_SECONDS
    timeout_seconds: float = RESULT_TIMEOUT_SECONDS
    headless: bool = True

    @classmethod
    def load(cls, path: Path) -> "WorkContext":
        raw = json.loads(path.read_text(encoding="utf-8"))
        document_id = int(raw["document_id"])
        if document_id not in DOCUMENT_ROUTES:
            raise ValueError("document_id no soportado")
        entry_url = str(raw["entry_url"])
        parsed = urlparse(entry_url)
        if parsed.scheme != "https" or parsed.hostname != SRI_HOST:
            raise ValueError("entry_url debe pertenecer al portal HTTPS autorizado")
        if parsed.path.rstrip("/") != DOCUMENT_ROUTES[document_id]:
            raise ValueError("entry_url no coincide con el documento configurado")
        identification = str(raw["identification"]).strip()
        if not identification:
            raise ValueError("identification requerida por el contexto autorizado")
        pacing = max(MIN_PACING_SECONDS, float(raw.get("pacing_seconds", MIN_PACING_SECONDS)))
        timeout = min(RESULT_TIMEOUT_SECONDS, max(10.0, float(raw.get("timeout_seconds", RESULT_TIMEOUT_SECONDS))))
        return cls(document_id, entry_url, identification, Path(raw["evidence_dir"]), pacing, timeout,
                   bool(raw.get("headless", True)))


class ActionPacer:
    def __init__(self, interval: float) -> None:
        self.interval = max(MIN_PACING_SECONDS, interval)
        self.last_action: float | None = None

    async def before_action(self) -> None:
        if self.last_action is not None:
            remaining = self.interval - (time.monotonic() - self.last_action)
            if remaining > 0:
                await asyncio.sleep(remaining)

    def mark(self) -> None:
        self.last_action = time.monotonic()


async def _visible_text(page) -> str:
    # Results are read only from the visible page; never use hidden app state.
    main = page.locator("main")
    if await main.count():
        return (await main.first.inner_text()).casefold()
    return (await page.locator("body").inner_text()).casefold()


def _classify(document_id: int, text: str, identification: str,
              baseline_text: str = "") -> str | None:
    folded = unicodedata.normalize("NFKD", text.casefold())
    normalized = "".join(char for char in folded if not unicodedata.combining(char))
    baseline_folded = unicodedata.normalize("NFKD", baseline_text.casefold())
    baseline = "".join(char for char in baseline_folded if not unicodedata.combining(char))
    no_match = re.search(r"no se encontraron resultados|no existen resultados", normalized)
    if no_match and no_match.group(0) not in baseline:
        return "NO_MATCH"
    positive_marker = ("al dia en sus obligaciones" if document_id == 3 else "activo")
    positive = positive_marker in normalized
    if positive:
        digits = re.sub(r"\D", "", identification)
        if 10 <= len(digits) <= 13:
            token = rf"(?<!\d)\d(?:[\s.-]?\d){{{len(digits) - 1}}}(?!\d)"
            if any(re.sub(r"\D", "", item) == digits
                   for item in re.findall(token, text)):
                return "MATCH"
        # SRI's static explanatory copy contains the same phrase as a possible
        # status. It is not a result unless it appears after submission and is
        # bound to the exact queried identifier.
        if positive_marker not in baseline:
            return "MATCH_NOT_ATTRIBUTED"
    return None


def _navigation_failure(exc: Exception) -> str:
    """Return a stable, sanitized reason for navigation/network failures."""
    if isinstance(exc, PlaywrightTimeoutError):
        return "PORTAL_NAVIGATION_TIMEOUT"
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
    return next((reason for marker, reason in markers if marker in message),
                "PORTAL_OR_BROWSER_ERROR")


async def _document_form_ready(page, context: WorkContext) -> bool:
    """Recognize a route that finished loading despite a late navigation error.

    This checks the already-open page only; it does not retry or reload the
    public portal. It lets a valid browser checkpoint continue safely.
    """
    try:
        landed = urlparse(page.url)
        if (landed.hostname != SRI_HOST or
                landed.path.rstrip("/") != DOCUMENT_ROUTES[context.document_id]):
            return False
        field = page.locator("#busquedaRucId")
        deadline = time.monotonic() + min(5.0, context.timeout_seconds)
        while time.monotonic() < deadline:
            if await field.count() == 1 and await field.is_visible():
                return True
            await page.wait_for_timeout(250)
        return False
    except Exception:
        return False


async def _execute_work(work, services, document_id: int) -> dict[str, str | None]:
    """Entry point used by the stable motor's generic external-adapter ABI."""
    global _human_barrier
    if work.portal_id != 3 or work.document_id != document_id:
        return {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}
    if _human_barrier:
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE",
                "reason_code": "PORTAL_CHALLENGE"}
    parsed = urlparse(work.entry_url)
    if (parsed.scheme != "https" or parsed.hostname != SRI_HOST or
            parsed.path.rstrip("/") != DOCUMENT_ROUTES[document_id]):
        return {"kind": "ERROR", "reason_code": "UNAUTHORIZED_ENTRY_URL"}
    browser = services["browser"]
    await browser.goto(work.entry_url)
    challenge = 'iframe[src*="captcha"], [class*="altcha"]'
    if await browser.is_visible(challenge):
        _human_barrier = True
        return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
    label = "RUC / cédula" if document_id == 3 else "RUC"
    # Angular validation in SRI listens to keyboard events. The motor's generic
    # type_text operation preserves its pacing policy while activating them.
    await browser.fill_role("textbox", label, "")
    await browser.type_text("#busquedaRucId", work.subject.identification)
    enable_deadline = time.monotonic() + min(work.deadline_seconds, 120)
    while time.monotonic() < enable_deadline:
        if await browser.enabled('button:has-text("Consultar")'):
            break
        await asyncio.sleep(0.5)
    if not await browser.enabled('button:has-text("Consultar")'):
        return {"kind": "RETRYABLE", "reason_code": "QUERY_NOT_ENABLED"}
    await browser.click_role("button", "Consultar", exact=True)
    deadline = time.monotonic() + min(work.deadline_seconds, 120)
    while time.monotonic() < deadline:
        if await browser.is_visible(challenge):
            _human_barrier = True
            return {"kind": "HUMAN_REQUIRED", "checkpoint": "PORTAL_CHALLENGE"}
        text = (await browser.text("body")).casefold()
        status = _classify(document_id, text, work.subject.identification)
        if status:
            evidence = Path(services["evidence_root"]) / f"sri-{document_id}-{work.detail_id}.png"
            await browser.screenshot(str(evidence), full_page=True)
            return {"kind": status, "evidence_path": str(evidence)}
        await asyncio.sleep(0.5)
    return {"kind": "RETRYABLE", "reason_code": "RESULT_NOT_CONCLUSIVE"}


async def documento_3(work, services):
    return await _execute_work(work, services, 3)


async def documento_53(work, services):
    return await _execute_work(work, services, 53)


DOCUMENT_FUNCTIONS = {"documento_3": documento_3, "documento_53": documento_53}


async def prepare(_work, _services):
    """Reset human barrier once per sidecar batch, not per document."""
    global _human_barrier
    _human_barrier = False


def _result(context: WorkContext, status: str, reason: str | None = None,
            evidence_sha256: str | None = None) -> dict[str, str | int | None]:
    return {"adapter_id": ADAPTER_ID, "adapter_version": ADAPTER_VERSION,
            "document_id": context.document_id, "status": status,
            "reason_code": reason, "evidence_sha256": evidence_sha256}


async def _run_on_page(context: WorkContext, page) -> dict[str, str | int | None]:
    context.evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = context.evidence_dir / f"sri-{context.document_id}-{time.time_ns()}.png"
    pacer = ActionPacer(context.pacing_seconds)
    try:
        # The document URL supplied by ORDS is the sole entry point. The portal
        # base URL is informational and must never replace this document route.
        response = await page.goto(context.entry_url, wait_until="commit",
                                   timeout=int(NAVIGATION_TIMEOUT_SECONDS * 1000))
    except Exception as exc:
        # Preserve a usable SPA checkpoint if the navigation event reports an
        # error after the exact document URL and its form have already loaded.
        # Never send a second navigation request as an automatic retry.
        if not await _document_form_ready(page, context):
            return _result(context, "RETRYABLE", _navigation_failure(exc))
        response = None
    try:
        if response and response.status in (403, 429, 451):
            return _result(context, "BLOCKED", f"HTTP_{response.status}")
        landed = urlparse(page.url)
        if landed.hostname != SRI_HOST:
            return _result(context, "RETRYABLE", "DOCUMENT_URL_REDIRECTED_OUTSIDE_PORTAL")
        if landed.path.rstrip("/") != DOCUMENT_ROUTES[context.document_id]:
            reason = "PORTAL_AUTH_REDIRECT" if landed.path.startswith("/auth/") else "DOCUMENT_URL_REDIRECTED"
            return _result(context, "RETRYABLE", reason)
    except Exception:
        return _result(context, "RETRYABLE", "DOCUMENT_URL_NOT_READY")
    pacer.mark()

    if await page.locator('iframe[src*="captcha"], [class*="altcha"]').count():
        return _result(context, "HUMAN_REQUIRED", "PORTAL_CHALLENGE")

    search_mode = ("Seleccionar búsqueda por RUC o cédula" if context.document_id == 3
                   else "Seleccionar búsqueda por RUC")
    mode_button = page.get_by_role("button", name=search_mode, exact=True)
    if await mode_button.count() == 1:
        await pacer.before_action()
        await mode_button.click(timeout=int(ELEMENT_TIMEOUT_SECONDS * 1000))
        pacer.mark()

    field = page.locator("#busquedaRucId")
    try:
        await field.wait_for(state="visible", timeout=int(ELEMENT_TIMEOUT_SECONDS * 1000))
    except PlaywrightTimeoutError:
        return _result(context, "RETRYABLE", "FORM_FIELD_NOT_READY")
    if await field.count() != 1:
        return _result(context, "RETRYABLE", "EXPECTED_FIELD_NOT_UNIQUE")
    await pacer.before_action()
    await field.fill("", timeout=int(ELEMENT_TIMEOUT_SECONDS * 1000))
    await field.click(timeout=int(ELEMENT_TIMEOUT_SECONDS * 1000))
    await page.keyboard.type(context.identification, delay=100)
    pacer.mark()

    button = page.get_by_role("button", name="Consultar", exact=True)
    await button.wait_for(state="visible", timeout=int(ELEMENT_TIMEOUT_SECONDS * 1000))
    await button.wait_for(state="attached", timeout=int(ELEMENT_TIMEOUT_SECONDS * 1000))
    enable_deadline = time.monotonic() + min(context.timeout_seconds, 30)
    while not await button.is_enabled() and time.monotonic() < enable_deadline:
        await page.wait_for_timeout(250)
    if not await button.is_enabled():
        return _result(context, "RETRYABLE", "QUERY_NOT_ENABLED")
    baseline_text = await _visible_text(page)
    await pacer.before_action()
    await button.click(timeout=int(ELEMENT_TIMEOUT_SECONDS * 1000))
    pacer.mark()

    deadline = time.monotonic() + context.timeout_seconds
    status = None
    stable_status = None
    stable_since = None
    unattributed_positive = False
    while time.monotonic() < deadline:
        text = await _visible_text(page)
        normalized_text = unicodedata.normalize("NFKD", text.casefold())
        normalized_text = "".join(char for char in normalized_text
                                  if not unicodedata.combining(char))
        if re.search(r"captcha|altcha|no soy un robot", normalized_text):
            return _result(context, "HUMAN_REQUIRED", "PORTAL_CHALLENGE")
        if re.search(r"espere por favor|\bcargando\b|\bprocesando\b", normalized_text):
            stable_status = None
            stable_since = None
            await page.wait_for_timeout(500)
            continue
        status = _classify(context.document_id, text, context.identification, baseline_text)
        if status == "MATCH_NOT_ATTRIBUTED":
            unattributed_positive = True
            status = None
        if status in {"MATCH", "NO_MATCH"}:
            if status != stable_status:
                stable_status = status
                stable_since = time.monotonic()
            elif time.monotonic() - stable_since >= 0.25:
                break
        else:
            stable_status = None
            stable_since = None
        await page.wait_for_timeout(500)

    if status is None:
        reason = "MATCH_NOT_ATTRIBUTED" if unattributed_positive else "RESULT_NOT_CONCLUSIVE"
        return _result(context, "RETRYABLE", reason)

    await page.screenshot(path=str(evidence_path), full_page=True)
    digest = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
    return _result(context, status, evidence_sha256=digest)


async def _launch_browser(playwright, headless: bool):
    # For headed debugging, prefer Chrome because the live portal inspection
    # for this candidate is performed in Chrome. Production headless keeps the
    # engine's contracted Edge-first order.
    channels = ("chrome", "msedge") if not headless else ("msedge", "chrome")
    for channel in channels:
        try:
            return await playwright.chromium.launch(channel=channel, headless=headless)
        except Exception:
            continue
    return None


async def _run(context: WorkContext) -> dict[str, str | int | None]:
    async with async_playwright() as playwright:
        browser = await _launch_browser(playwright, context.headless)
        if browser is None:
            return _result(context, "ERROR", "NO_SUPPORTED_BROWSER")
        try:
            page = await browser.new_page()
            return await _run_on_page(context, page)
        finally:
            await browser.close()


async def run_many(contexts: list[WorkContext]) -> list[dict[str, str | int | None]]:
    """Run ORDS-ordered SRI work in one browser session; isolate each work failure."""
    if not contexts:
        return []
    async with async_playwright() as playwright:
        browser = await _launch_browser(playwright, contexts[0].headless)
        if browser is None:
            return [_result(context, "ERROR", "NO_SUPPORTED_BROWSER") for context in contexts]
        try:
            page = await browser.new_page()
            results = []
            for context in contexts:
                try:
                    result = await _run_on_page(context, page)
                except PlaywrightTimeoutError:
                    result = _result(context, "RETRYABLE", "PORTAL_TIMEOUT")
                except Exception as exc:
                    result = _result(context, "RETRYABLE", _navigation_failure(exc))
                results.append(result)
            return results
        finally:
            await browser.close()


async def run(context: WorkContext) -> dict[str, str | int | None]:
    """Mapear fallos de portal/red posteriores al launch a un resultado recuperable."""
    try:
        return await _run(context)
    except PlaywrightTimeoutError:
        return {"adapter_id": ADAPTER_ID, "adapter_version": ADAPTER_VERSION,
                "document_id": context.document_id, "status": "RETRYABLE",
                "reason_code": "PORTAL_TIMEOUT", "evidence_sha256": None}
    except Exception as exc:
        # No publicar URLs, datos de sujeto ni texto privado de excepciones.
        return {"adapter_id": ADAPTER_ID, "adapter_version": ADAPTER_VERSION,
                "document_id": context.document_id, "status": "RETRYABLE",
                "reason_code": _navigation_failure(exc), "evidence_sha256": None}


def main() -> int:
    parser = argparse.ArgumentParser(description="SRI standalone TEST adapter")
    parser.add_argument("--context", required=True, type=Path, action="append",
                        help="JSON privado entregado por el harness autorizado TEST; repeat for ORDS order")
    parser.add_argument("--headed", action="store_true", help="usar ventana de navegador para depuración")
    args = parser.parse_args()
    try:
        repo_root = Path(__file__).resolve().parents[2]
        contexts = []
        for context_path in args.context:
            context_path = context_path.resolve()
            if context_path.is_relative_to(repo_root):
                raise ValueError("el contexto privado debe estar fuera del repositorio")
            context = WorkContext.load(context_path)
            if args.headed:
                context = WorkContext(context.document_id, context.entry_url, context.identification,
                                      context.evidence_dir, context.pacing_seconds,
                                      context.timeout_seconds, False)
            if context.evidence_dir.resolve().is_relative_to(repo_root):
                raise ValueError("la evidencia privada debe estar fuera del repositorio")
            contexts.append(context)
        results = asyncio.run(run_many(contexts))
    except Exception as exc:
        # Deliberately emit only a stable category, not exception text or input values.
        print(json.dumps({"adapter_id": ADAPTER_ID, "adapter_version": ADAPTER_VERSION,
                          "status": "ERROR", "reason_code": "INVALID_CONTEXT_OR_RUNTIME",
                          "exception_type": type(exc).__name__}, ensure_ascii=False))
        return 2
    print(json.dumps(results, ensure_ascii=False))
    return 0 if all(result["status"] in {"MATCH", "NO_MATCH"} for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())

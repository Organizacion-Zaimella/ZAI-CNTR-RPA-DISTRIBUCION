# Lista Clinton adapter candidate 0.1.4

Adapter ID `lista_clinton`; portal 5 (OFAC), Oracle document 33. The standalone Playwright application downloads
the configured public Treasury SDN PDF and searches all extractable text pages
using the legacy workflow's normalized full-name match. A `NO_MATCH` result is
conclusive only when every PDF page has searchable text; OCR is not used. The
bundle keeps the source PDF and a search receipt together.

The signed TEST release for candidate 0.1.3 is available at
[`cntr-rpa-lista-clinton-0.1.3-test1`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-lista-clinton-0.1.3-test1).
It was downloaded and verified by the isolated engine updater. No current ORDS
eligible pair or function assignment exists for document 33, so the release did
not produce a subject search, document evidence, or ACK. Candidate 0.1.4 adds a
bounded page-number list to standalone JSON while retaining the total number of
matching pages and all matching page references in the private PDF receipt.

`app.py` runs independently with a private JSON context. `adapter.py` is the
motor ABI entrypoint. `dependencies.lock` pins Playwright and PyMuPDF. The
Playwright `APIRequestContext` retrieves original PDF bytes directly:
`page.goto()` on a PDF URL returns Chromium's internal HTML viewer wrapper, not
the binary. The download has a 90-second total ceiling, rejects redirects,
validates MIME, length and `%PDF-`, and spaces repeated list downloads by at
least five seconds. Viewer-wrapper or partial bytes are never evidence.
Browser transport failures map to bounded codes; exception text, URLs and query
names are never included in standard output.

The 2026-10-10 local full-PDF check downloaded a public 3,232-page SDN document
and exercised `search_and_bundle` locally. A phrase found on one source page
returned `MATCH`; the generated receipt-plus-source PDF passed structural
validation. A separate common phrase matched 3,232 pages; this exposed the
unbounded `matched_pages` response. Candidate 0.1.4 caps that JSON field at 30
page numbers, reports the full `match_count`, and marks truncation. The query
phrase and resulting PDF remain private. This is a local parser/app test, not a
subject-specific capture, ORDS execution, or certification for document 33.

Synthetic regression tests use local PDFs only and do not contact Treasury or
ORDS. A public PDF phrase test does not create a subject master or send a search
to the portal. Current Oracle TEST has no eligible pair/adapter assignment for
doc. 33; do not force the robot test or alter eligibility to enable it.

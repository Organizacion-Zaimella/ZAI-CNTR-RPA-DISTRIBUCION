# Lista Clinton adapter candidate 0.1.2

Portal 134, Oracle document 33. The standalone Playwright application downloads
the configured public Treasury SDN PDF and searches all extractable text pages
using the legacy workflow's normalized full-name match. A `NO_MATCH` result is
only conclusive when every PDF page has searchable text; OCR is not used. The
bundle keeps the source PDF and a search receipt together.

The historical C.106 workflow 63/v8 (document 33) is a behavior reference,
not certification of this independent adapter. No current ORDS eligible pair
was present in the latest snapshot. This candidate has not queried a subject,
has no signed release, and remains `NOT_APPROVED`.

`app.py` runs independently with a private JSON context. `src/adapter.py` is
the motor ABI entrypoint. `dependencies.lock` pins Playwright and PyMuPDF.
The Playwright `APIRequestContext` retrieves original PDF bytes directly:
`page.goto()` on a PDF URL returns Chromium's internal HTML viewer wrapper, not
the binary. The download has a 90-second total ceiling, rejects redirects,
validates MIME, length and `%PDF-`, and spaces repeated list downloads by at
least five seconds. Viewer-wrapper or partial bytes are never evidence.
Synthetic checks use local PDFs only and do not contact Treasury or ORDS.
Browser transport failures map to bounded codes such as `NETWORK_DISCONNECTED`,
`PORTAL_DNS_FAILURE`, `PORTAL_TIMEOUT`, and `PORTAL_UNREACHABLE`; exception text
and URLs are never included in the result. A local synthetic sequence verifies
that the next ORDS-ordered work continues after a transient download failure.
The document URL opened in Chrome and displayed the Treasury PDF (3,232 pages).
The old `page.goto()` acquisition exposed a 348-byte internal viewer wrapper
despite the PDF MIME header. Candidate 0.1.2 changes to raw Playwright API
requests; a subject-free binary check retrieved the 16,539,778-byte PDF with a
valid signature. This verifies transport only: no subject was searched. There
is no current eligible ORDS pair, signed release, or ACK, so this is not a live
document certification.

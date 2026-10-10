# Lista Clinton adapter candidate 0.1.1

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
PDF navigation has a 30-second start budget and transfer gets up to 60 more
seconds (90 seconds total). A transfer timeout returns retryable; partial bytes
are never inspected or accepted as evidence.
Synthetic checks use local PDFs only and do not contact Treasury or ORDS.
Browser transport failures map to bounded codes such as `NETWORK_DISCONNECTED`,
`PORTAL_DNS_FAILURE`, `PORTAL_TIMEOUT`, and `PORTAL_UNREACHABLE`; exception text
and URLs are never included in the result. A local synthetic sequence verifies
that the next ORDS-ordered work can use the same browser session after a
transient network failure. Eleven offline tests cover the bounded PDF wait.
A browser inspection opened the configured document URL, but the PDF viewer
exposed no accessible text. One Python acquisition returned HTTP 200 and
`application/pdf`, while its body was only 348 bytes of HTML; the application
rejected it as `PDF_SIGNATURE_INVALID`. No subject was searched. There is no
current eligible ORDS pair, signed release, or ACK, so this is not a live
document certification.

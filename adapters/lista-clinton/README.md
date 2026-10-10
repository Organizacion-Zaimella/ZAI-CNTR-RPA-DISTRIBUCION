# Lista Clinton adapter candidate 0.1.0

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
Synthetic checks use local PDFs only and do not contact Treasury or ORDS.
Browser transport failures map to bounded codes such as `NETWORK_DISCONNECTED`,
`PORTAL_DNS_FAILURE`, `PORTAL_TIMEOUT`, and `PORTAL_UNREACHABLE`; exception text
and URLs are never included in the result. A local synthetic sequence verifies
that the next ORDS-ordered work can use the same browser session after a
transient network failure. Ten offline tests pass; this is not a live portal
certification or an ORDS ACK.

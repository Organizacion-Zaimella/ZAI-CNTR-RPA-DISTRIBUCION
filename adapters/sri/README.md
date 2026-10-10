# SRI adapter candidate 0.1.7

TEST candidate for SRI portal 3, documents 3 and 53. `app.py` is the
independent Playwright entrypoint; `src/adapter.py` is the isolated motor ABI.
This package is **not certified** and is not pinned by the current ORDS TEST
plan.

The sidecar validates the HTTPS host and document route, selects the
document-specific search mode, checks the search field is unique, types through
the motor's paced browser API, and returns sanitized retryable outcomes for
timeouts or uncertain results. It uses the optional `goto_commit` capability
for the SRI client-rendered form and falls back to the existing `goto` ABI when
running under an older installed 1.0.0 engine. CAPTCHA and other human
challenges are never solved or bypassed. The standalone result polling ignores the visible loading overlay, excludes static pre-query help text, requires stable visible MATCH/NO_MATCH for 250 ms, and binds MATCH to the queried RUC. A real headed TEST run of documents 3 and 53 returned MATCH in ORDS order with private PNG evidence. Headless mode timed out at navigation on this host; it is not treated as portal outage.

Run synthetic contract checks with `python -m pytest adapters/sri/tests -q`.
They use fake browser services and make no network requests. The package still
requires a legitimate real-browser run in authorized TEST, signed publication,
compatible ORDS assignment, and evidence plus ACK through the installed motor
before certification.

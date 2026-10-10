# OFAC adapter candidate 0.1.2

TEST candidate for OFAC document 5. `app.py` is the independent Playwright
entrypoint; `src/adapter.py` is the isolated motor ABI. This candidate is not
certified and must not be promoted to Production.

The standalone application searches by the authorized subject name, classifies
only the visible `Lookup Results` count, and stores a full-page screenshot
outside the repository. The sidecar validates the HTTPS host and returns
sanitized retryable outcomes for network loss and timeouts. HTTP 403/429/451
and human challenges do not trigger a repeated request. CAPTCHA is never
solved or bypassed.

Run synthetic checks using `python -m pytest adapters/ofac/tests -q`. They use
fake browser objects and make no portal requests. Coverage includes HTTP 403
and 429, challenges before and after sending, network loss with ordered
continuation, evidence hashing, and inconclusive results without evidence. Real
TEST certification still requires an authorized browser run, signed
distribution and evidence plus ACK from the installed motor.

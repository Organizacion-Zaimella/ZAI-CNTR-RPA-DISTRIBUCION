import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace

MODULE = Path(__file__).parents[1] / "src" / "adapter.py"
SPEC = importlib.util.spec_from_file_location("adapter_candidate", MODULE)
ADAPTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADAPTER)


def test_catalog_functions_are_callable():
    assert ADAPTER.DOCUMENT_FUNCTIONS
    assert all(callable(function) for function in ADAPTER.DOCUMENT_FUNCTIONS.values())


def test_wrong_portal_fails_closed_before_browser():
    for function in ADAPTER.DOCUMENT_FUNCTIONS.values():
        document_id = int(function.__name__.split("documento_")[-1])
        work = SimpleNamespace(portal_id=-1, document_id=document_id)
        result = asyncio.run(function(work, {}))
        assert result == {"kind": "ERROR", "reason_code": "UNSUPPORTED_DOCUMENT"}

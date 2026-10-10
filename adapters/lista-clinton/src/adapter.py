"""Motor ABI for Lista Clinton document 33."""
from __future__ import annotations

from app import DOCUMENT_FUNCTIONS, documento_33


async def execute_document(work, services):
    return await documento_33(work, services)


async def prepare(_work, _services):
    """No persistent portal state is required by this PDF-based adapter."""
    return None

# ============================================================================
# app/crud/__init__.py
# ============================================================================
"""CRUD operations package."""

from app.crud.user import CRUDUser
from app.crud.language import CRUDLanguage
from app.crud.doc_section import CRUDDocSection

# Create instances
user = CRUDUser(User)
language = CRUDLanguage(Language)
doc_section = CRUDDocSection(DocSection)

__all__ = [
    "user",
    "language",
    "doc_section",
]
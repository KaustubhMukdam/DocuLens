# ============================================================================
# app/crud/__init__.py
# ============================================================================
"""CRUD operations package."""

from app.crud.user import CRUDUser
from app.crud.language import CRUDLanguage
from app.crud.doc_section import CRUDDocSection
from app.models.user import User
from app.models.language import Language
from app.models.doc_section import DocSection

# Create instances
user = CRUDUser(User)
language = CRUDLanguage(Language)
doc_section = CRUDDocSection(DocSection)

__all__ = [
    "user",
    "language",
    "doc_section",
]
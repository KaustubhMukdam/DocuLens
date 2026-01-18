"""
Documentation section schemas for request/response.
"""

from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from app.models.doc_section import Difficulty


class DocSectionBase(BaseModel):
    """Base doc section schema."""
    title: str = Field(..., max_length=255)
    slug: str = Field(..., max_length=255)
    content_raw: str
    content_summary: Optional[str] = None
    source_url: str
    order_index: int = 0
    estimated_time_minutes: Optional[int] = None
    difficulty: Difficulty = Difficulty.MEDIUM
    is_quick_path: bool = False
    is_deep_path: bool = True


class DocSectionCreate(DocSectionBase):
    """Schema for creating a doc section."""
    language_id: UUID
    parent_id: Optional[UUID] = None


class DocSectionUpdate(BaseModel):
    """Schema for updating a doc section."""
    title: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    content_raw: Optional[str] = None
    content_summary: Optional[str] = None
    source_url: Optional[str] = None
    order_index: Optional[int] = None
    estimated_time_minutes: Optional[int] = None
    difficulty: Optional[Difficulty] = None
    is_quick_path: Optional[bool] = None
    is_deep_path: Optional[bool] = None
    parent_id: Optional[UUID] = None


class DocSectionSummary(BaseModel):
    """Schema for doc section summary/minimal info."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    slug: str
    order_index: int
    difficulty: Difficulty
    estimated_time_minutes: Optional[int]
    is_quick_path: bool
    is_deep_path: bool


class DocSectionResponse(BaseModel):
    """Schema for doc section response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    language_id: UUID
    parent_id: Optional[UUID]
    title: str
    slug: str
    content_raw: str
    content_summary: Optional[str]
    source_url: str
    order_index: int
    estimated_time_minutes: Optional[int]
    difficulty: Difficulty
    is_quick_path: bool
    is_deep_path: bool
    created_at: datetime
    updated_at: datetime


class DocSectionDetailResponse(DocSectionResponse):
    """Schema for doc section detailed response including children."""
    children: list["DocSectionDetailResponse"] = []

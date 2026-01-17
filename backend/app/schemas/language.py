# ============================================================================
# app/schemas/language.py
# ============================================================================
"""Language schemas."""

from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class LanguageBase(BaseModel):
    """Base language schema."""
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    official_doc_url: str
    description: Optional[str] = None
    version: Optional[str] = Field(None, max_length=20)


class LanguageCreate(LanguageBase):
    """Schema for creating a language."""
    logo_url: Optional[str] = None


class LanguageUpdate(BaseModel):
    """Schema for updating a language."""
    official_doc_url: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    is_active: Optional[bool] = None


class LanguageResponse(BaseModel):
    """Schema for language response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    slug: str
    official_doc_url: str
    logo_url: Optional[str]
    description: Optional[str]
    version: Optional[str]
    is_active: bool
    last_updated: Optional[datetime]
    created_at: datetime


class LanguageDetailResponse(LanguageResponse):
    """Extended language response with statistics."""
    total_sections: int = 0
    quick_path_sections: int = 0
    deep_path_sections: int = 0
    estimated_quick_time_hours: float = 0.0
    estimated_deep_time_hours: float = 0.0


# ============================================================================
# app/schemas/doc_section.py
# ============================================================================
"""Documentation section schemas."""

from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class DocSectionBase(BaseModel):
    """Base documentation section schema."""
    title: str = Field(..., max_length=255)
    slug: str = Field(..., max_length=255)
    content_raw: str
    source_url: str
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")


class DocSectionCreate(DocSectionBase):
    """Schema for creating a documentation section."""
    language_id: UUID
    parent_id: Optional[UUID] = None
    content_summary: Optional[str] = None
    order_index: int = 0
    estimated_time_minutes: Optional[int] = None
    is_quick_path: bool = False
    is_deep_path: bool = True


class DocSectionUpdate(BaseModel):
    """Schema for updating a documentation section."""
    title: Optional[str] = None
    content_raw: Optional[str] = None
    content_summary: Optional[str] = None
    source_url: Optional[str] = None
    order_index: Optional[int] = None
    estimated_time_minutes: Optional[int] = None
    difficulty: Optional[str] = None
    is_quick_path: Optional[bool] = None
    is_deep_path: Optional[bool] = None


class DocSectionSummary(BaseModel):
    """Brief documentation section info."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    title: str
    slug: str
    difficulty: str
    estimated_time_minutes: Optional[int]
    is_completed: bool = False


class CodeExampleResponse(BaseModel):
    """Code example response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    title: Optional[str]
    code: str
    language: str
    explanation: Optional[str]
    output: Optional[str]
    is_runnable: bool
    order_index: int


class DocSectionResponse(BaseModel):
    """Schema for documentation section response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    language_id: UUID
    parent_id: Optional[UUID]
    title: str
    slug: str
    content_summary: Optional[str]
    source_url: str
    order_index: int
    estimated_time_minutes: Optional[int]
    difficulty: str
    is_quick_path: bool
    is_deep_path: bool


class DocSectionDetailResponse(DocSectionResponse):
    """Extended section response with full content."""
    content_raw: str
    code_examples: List[CodeExampleResponse] = []
    has_next: bool = False
    has_prev: bool = False
    next_section_id: Optional[UUID] = None
    prev_section_id: Optional[UUID] = None


# ============================================================================
# app/schemas/learning_path.py
# ============================================================================
"""Learning path schemas."""

from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class LearningPathCreate(BaseModel):
    """Schema for creating a learning path."""
    language_id: UUID
    path_type: str = Field(..., pattern="^(quick|deep)$")


class LearningPathUpdate(BaseModel):
    """Schema for updating a learning path."""
    status: Optional[str] = Field(None, pattern="^(not_started|in_progress|completed)$")
    progress_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)


class LearningPathResponse(BaseModel):
    """Schema for learning path response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    language_id: UUID
    path_type: str
    status: str
    progress_percentage: float
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime


class LearningPathDetailResponse(LearningPathResponse):
    """Extended learning path with sections."""
    language_name: str
    language_slug: str
    total_sections: int = 0
    completed_sections: int = 0
    estimated_time_hours: float = 0.0
    sections: List[DocSectionSummary] = []


# ============================================================================
# app/schemas/progress.py
# ============================================================================
"""Progress tracking schemas."""

from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class MarkCompleteRequest(BaseModel):
    """Request to mark a section as complete."""
    doc_section_id: UUID
    time_spent_seconds: int = Field(..., ge=0)
    notes: Optional[str] = None


class UserProgressResponse(BaseModel):
    """User progress response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    doc_section_id: UUID
    is_completed: bool
    time_spent_seconds: int
    completed_at: Optional[datetime]
    notes: Optional[str]


class ProgressStatsResponse(BaseModel):
    """User progress statistics."""
    total_time_seconds: int
    total_time_hours: float
    sections_completed: int
    current_streak_days: int
    longest_streak_days: int
    languages_learning: int
    active_paths: int
    completed_paths: int
    achievements: List[str] = []


# ============================================================================
# app/schemas/bookmark.py
# ============================================================================
"""Bookmark schemas."""

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BookmarkCreate(BaseModel):
    """Schema for creating a bookmark."""
    doc_section_id: UUID
    notes: Optional[str] = None


class BookmarkUpdate(BaseModel):
    """Schema for updating a bookmark."""
    notes: Optional[str] = None


class BookmarkResponse(BaseModel):
    """Schema for bookmark response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    doc_section_id: UUID
    notes: Optional[str]
    created_at: datetime
    
    # Related section info
    section_title: Optional[str] = None
    section_slug: Optional[str] = None
    language_name: Optional[str] = None


# ============================================================================
# app/schemas/__init__.py
# ============================================================================
"""Schemas package."""

from app.schemas.response import (
    SuccessResponse,
    ErrorResponse,
    PaginationMeta,
    PaginatedResponse
)
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    ChangePasswordRequest
)
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserProfileResponse
)

__all__ = [
    # Response
    "SuccessResponse",
    "ErrorResponse",
    "PaginationMeta",
    "PaginatedResponse",
    # Auth
    "RegisterRequest",
    "LoginRequest",
    "TokenResponse",
    "RefreshTokenRequest",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "ChangePasswordRequest",
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserProfileResponse",
]
"""
Base model class with common fields for all models.
"""

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4
import json

from sqlalchemy import DateTime, func, TypeDecorator, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID, ARRAY as PGARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.
    
    Uses PostgreSQL's UUID type when available, otherwise uses String(36).
    This allows the same model to work with both PostgreSQL (production) and SQLite (testing).
    """
    impl = String
    cache_ok = True
    
    def load_dialect_impl(self, dialect):
        """Use native UUID for PostgreSQL, String for others."""
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PGUUID(as_uuid=True))
        else:
            return dialect.type_descriptor(String(36))
    
    def process_bind_param(self, value, dialect):
        """Convert UUID to appropriate type for the database."""
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value  # PostgreSQL handles UUID natively
        else:
            return str(value)  # SQLite needs string
    
    def process_result_value(self, value, dialect):
        """Convert database value back to UUID."""
        if value is None:
            return value
        else:
            if isinstance(value, str):
                return UUID(value)
            return value


class StringArray(TypeDecorator):
    """
    Platform-independent ARRAY type for string arrays.
    
    Uses PostgreSQL's ARRAY type when available, otherwise uses JSON for SQLite.
    This allows the same model to work with both PostgreSQL (production) and SQLite (testing).
    """
    impl = Text
    cache_ok = True
    
    def load_dialect_impl(self, dialect):
        """Use native ARRAY for PostgreSQL, Text/JSON for others."""
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PGARRAY(String))
        else:
            return dialect.type_descriptor(Text)
    
    def process_bind_param(self, value, dialect):
        """Convert list to appropriate type for the database."""
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value  # PostgreSQL handles arrays natively
        else:
            return json.dumps(value)  # SQLite needs JSON string
    
    def process_result_value(self, value, dialect):
        """Convert database value back to list."""
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value  # PostgreSQL returns list already
        else:
            return json.loads(value) if value else []


class Base(DeclarativeBase):
    """Base class for all database models."""
    
    # Common columns for all models
    id: Mapped[UUID] = mapped_column(
        GUID(),  # Use platform-independent GUID instead of PGUUID
        primary_key=True,
        default=uuid4,
        index=True
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert model instance to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self) -> str:
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={self.id})>"
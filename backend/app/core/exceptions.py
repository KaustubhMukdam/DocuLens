"""
Custom exception classes for the application.
"""

from typing import Any, Optional


class DocuLensException(Exception):
    """Base exception for DocuLens application."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Any] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class NotFoundException(DocuLensException):
    """Exception raised when a resource is not found."""
    
    def __init__(
        self,
        message: str = "Resource not found",
        details: Optional[Any] = None
    ):
        super().__init__(message=message, status_code=404, details=details)


class UnauthorizedException(DocuLensException):
    """Exception raised when authentication fails."""
    
    def __init__(
        self,
        message: str = "Unauthorized",
        details: Optional[Any] = None
    ):
        super().__init__(message=message, status_code=401, details=details)


class ForbiddenException(DocuLensException):
    """Exception raised when access is forbidden."""
    
    def __init__(
        self,
        message: str = "Forbidden",
        details: Optional[Any] = None
    ):
        super().__init__(message=message, status_code=403, details=details)


class BadRequestException(DocuLensException):
    """Exception raised when request is invalid."""
    
    def __init__(
        self,
        message: str = "Bad request",
        details: Optional[Any] = None
    ):
        super().__init__(message=message, status_code=400, details=details)


class ConflictException(DocuLensException):
    """Exception raised when there's a conflict."""
    
    def __init__(
        self,
        message: str = "Conflict",
        details: Optional[Any] = None
    ):
        super().__init__(message=message, status_code=409, details=details)


class ValidationException(DocuLensException):
    """Exception raised when validation fails."""
    
    def __init__(
        self,
        message: str = "Validation error",
        details: Optional[Any] = None
    ):
        super().__init__(message=message, status_code=422, details=details)


class RateLimitException(DocuLensException):
    """Exception raised when rate limit is exceeded."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        details: Optional[Any] = None
    ):
        super().__init__(message=message, status_code=429, details=details)


class ExternalServiceException(DocuLensException):
    """Exception raised when external service fails."""
    
    def __init__(
        self,
        message: str = "External service error",
        details: Optional[Any] = None
    ):
        super().__init__(message=message, status_code=503, details=details)


class DatabaseException(DocuLensException):
    """Exception raised when database operation fails."""
    
    def __init__(
        self,
        message: str = "Database error",
        details: Optional[Any] = None
    ):
        super().__init__(message=message, status_code=500, details=details)
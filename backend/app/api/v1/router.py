# ============================================================================
# app/api/v1/router.py
# ============================================================================
"""API v1 router - aggregates all endpoint routers."""

from fastapi import APIRouter
from app.api.v1 import (
    auth, users, languages, docs, ai, learning_paths,
    progress, bookmarks, videos, practice, discussions,
    admin
)

api_router = APIRouter()

# Authentication
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# Users
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

# Languages
api_router.include_router(
    languages.router,
    prefix="/languages",
    tags=["Languages"]
)

# Documentation Sections (ADD THIS)
api_router.include_router(
    docs.router,
    prefix="/docs",
    tags=["Documentation"]
)

# AI Features
api_router.include_router(
    ai.router,
    prefix="/ai",
    tags=["AI & Summarization"]
)

# Learning Paths
api_router.include_router(
    learning_paths.router,
    prefix="/learning-paths",
    tags=["Learning Paths"]
)

# Progress Tracking
api_router.include_router(
    progress.router,
    prefix="/progress",
    tags=["Progress Tracking"]
)

# Bookmarks
api_router.include_router(
    bookmarks.router,
    prefix="/bookmarks",
    tags=["Bookmarks"]
)

# Video Resources
api_router.include_router(
    videos.router,
    prefix="/videos",
    tags=["Video Resources"]
)

# Practice Problems
api_router.include_router(
    practice.router,
    prefix="/practice",
    tags=["Practice Problems"]
)

# Discussions
api_router.include_router(
    discussions.router,
    prefix="/discussions",
    tags=["Discussions & Comments"]
)

# Admin
api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["👑 Admin Panel"]
)

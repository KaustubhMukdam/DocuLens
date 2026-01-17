# ============================================================================
# app/api/v1/router.py
# ============================================================================
"""Main API router combining all endpoint routers."""

from fastapi import APIRouter

from app.api.v1 import auth, users, languages, docs

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(languages.router, prefix="/languages", tags=["Languages"])
api_router.include_router(docs.router, prefix="/docs", tags=["Documentation"])
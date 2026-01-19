# ============================================================================
# app/scrapers/__init__.py
# ============================================================================
"""Web scraping modules for documentation and resources."""

from app.scrapers.base import BaseScraper
from app.scrapers.python_docs import PythonDocsScraper
from app.scrapers.youtube import YouTubeIntegration

__all__ = [
    "BaseScraper",
    "PythonDocsScraper",
    "YouTubeIntegration",
]

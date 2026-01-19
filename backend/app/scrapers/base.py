# ============================================================================
# app/scrapers/base.py
# ============================================================================
"""Base scraper class with common functionality."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import asyncio

from app.core.config import settings
from app.core.logging import logger


class BaseScraper(ABC):
    """Base class for all scrapers."""
    
    def __init__(self, base_url: str):
        """
        Initialize scraper.
        
        Args:
            base_url: Base URL of the documentation site
        """
        self.base_url = base_url
        self.session = None
        self.headers = {
            "User-Agent": settings.SCRAPING_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = httpx.AsyncClient(
            headers=self.headers,
            timeout=30.0,
            follow_redirects=True
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.aclose()
    
    async def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a single page.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None on error
        """
        try:
            logger.info(f"Fetching: {url}")
            response = await self.session.get(url)
            response.raise_for_status()
            
            # Rate limiting
            await asyncio.sleep(settings.SCRAPING_DELAY_SECONDS)
            
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content.
        
        Args:
            html: HTML string
            
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, "lxml")
    
    def make_absolute_url(self, url: str) -> str:
        """
        Convert relative URL to absolute.
        
        Args:
            url: Relative or absolute URL
            
        Returns:
            Absolute URL
        """
        return urljoin(self.base_url, url)
    
    def clean_text(self, text: str) -> str:
        """
        Clean extracted text.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = " ".join(text.split())
        return text.strip()
    
    @abstractmethod
    async def scrape_index(self) -> List[Dict[str, Any]]:
        """
        Scrape the documentation index/table of contents.
        
        Returns:
            List of section metadata
        """
        pass
    
    @abstractmethod
    async def scrape_section(self, url: str) -> Dict[str, Any]:
        """
        Scrape a single documentation section.
        
        Args:
            url: Section URL
            
        Returns:
            Section data
        """
        pass
    
    async def scrape_all(self) -> List[Dict[str, Any]]:
        """
        Scrape all documentation sections.
        
        Returns:
            List of all sections
        """
        logger.info(f"Starting scrape of {self.base_url}")
        
        # Get index
        index = await self.scrape_index()
        logger.info(f"Found {len(index)} sections in index")
        
        # DEBUG: Print first few index items
        if index:
            logger.info(f"Sample index item: {index[0]}")
        
        # Scrape each section
        sections = []
        for item in index:
            logger.info(f"Scraping section: {item.get('title')} from {item.get('url')}")
            section = await self.scrape_section(item["url"])
            
            if section:
                # Merge index metadata with scraped content
                full_section = {**item, **section}
                sections.append(full_section)
                logger.info(f"✓ Successfully scraped: {item.get('title')}")
            else:
                logger.warning(f"✗ Failed to scrape: {item.get('title')}")
        
        logger.info(f"Successfully scraped {len(sections)} sections")
        return sections

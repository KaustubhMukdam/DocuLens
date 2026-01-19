# ============================================================================
# app/scrapers/python_docs.py
# ============================================================================
"""Scraper for Python official documentation."""

from typing import List, Dict, Any, Optional
import re
from bs4 import BeautifulSoup, Tag

from app.scrapers.base import BaseScraper
from app.core.logging import logger


class PythonDocsScraper(BaseScraper):
    """Scraper for Python documentation."""
    
    def __init__(self, version: str = "3"):
        """
        Initialize Python docs scraper.
        
        Args:
            version: Python version (default: 3)
        """
        base_url = f"https://docs.python.org/{version}/tutorial/"  # FIX: Add /tutorial/
        super().__init__(base_url)
        self.version = version
    
    async def scrape_index(self) -> List[Dict[str, Any]]:
        """
        Scrape Python documentation index.
        
        Returns:
            List of tutorial sections
        """
        # Fetch tutorial index
        tutorial_url = self.make_absolute_url("index.html")
        html = await self.fetch_page(tutorial_url)
        
        if not html:
            logger.error("Failed to fetch tutorial index")
            return []
        
        soup = self.parse_html(html)
        sections = []
        
        # Find main content area
        content = soup.find("div", class_="body") or soup.find("section")
        if not content:
            logger.warning("Could not find tutorial content")
            return []
        
        # Find all section links (main tutorial pages only, not subsections)
        # We want links like "appetite.html", "interpreter.html", not "#subsection"
        links = content.find_all("a", class_="reference internal")
        
        seen_urls = set()
        order = 1
        
        for link in links:
            href = link.get("href", "")
            title = self.clean_text(link.get_text())
            
            # Skip empty, anchors, or external links
            if not href or href.startswith("#") or href.startswith("http"):
                continue
            
            # Only take .html files (main pages)
            if not href.endswith(".html"):
                continue
            
            # Avoid duplicates
            if href in seen_urls:
                continue
            
            # Skip index itself
            if "index.html" in href:
                continue
            
            seen_urls.add(href)
            
            # Construct absolute URL
            absolute_url = self.make_absolute_url(href)
            
            sections.append({
                "title": title,
                "url": absolute_url,
                "slug": self._generate_slug(title),
                "order_index": order,
                "difficulty": self._estimate_difficulty(order, title)
            })
            
            order += 1
            
            # Limit to first 15 main sections
            if order > 15:
                break
        
        logger.info(f"Extracted {len(sections)} tutorial sections")
        return sections
    
    async def scrape_section(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape a single Python documentation section.
        
        Args:
            url: Section URL
            
        Returns:
            Section data with content
        """
        html = await self.fetch_page(url)
        if not html:
            return None
        
        soup = self.parse_html(html)
        
        # Extract main content
        content = soup.find("div", class_="body") or soup.find("section")
        if not content:
            logger.warning(f"No content found for {url}")
            return None
        
        # Remove navigation elements
        for nav in content.find_all(["nav", "div"], class_=["sphinxsidebar", "related"]):
            nav.decompose()
        
        # Extract text (preserve some structure)
        paragraphs = []
        for p in content.find_all(["p", "h1", "h2", "h3", "li"]):
            text = self.clean_text(p.get_text())
            if text:
                paragraphs.append(text)
        
        raw_text = "\n\n".join(paragraphs)
        
        # Extract code examples
        code_examples = self._extract_code_examples(soup)
        
        # Estimate reading time
        word_count = len(raw_text.split())
        reading_time = max(10, (word_count // 200) * 5)  # ~200 words/min, round to 5 min
        
        logger.info(f"Scraped section: {url} ({word_count} words, {len(code_examples)} code examples)")
        
        return {
            "content_raw": raw_text[:50000],  # Limit to 50k chars
            "source_url": url,
            "estimated_time_minutes": reading_time,
            "code_examples": code_examples[:5],  # Max 5 examples
            "word_count": word_count
        }
    
    def _extract_code_examples(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract code examples from page."""
        examples = []
        
        # Find code blocks
        for idx, code_block in enumerate(soup.find_all(["pre", "div"], class_=["highlight", "highlight-python"]), start=1):
            # Get the actual code element
            code_elem = code_block.find("code") or code_block
            code = code_elem.get_text().strip()
            
            if code and len(code) < 5000 and len(code) > 10:  # Skip huge blocks and tiny ones
                examples.append({
                    "language": "python",
                    "code": code,
                    "order_index": idx
                })
                
                # Limit to 10 examples per page
                if len(examples) >= 10:
                    break
        
        return examples
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title."""
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_]+', '-', slug)
        return slug.strip('-')[:50]  # Limit length
    
    def _estimate_difficulty(self, order: int, title: str) -> str:
        """Estimate difficulty based on position and title."""
        title_lower = title.lower()
        
        # Advanced topics
        if any(word in title_lower for word in [
            "advanced", "decorator", "metaclass", "async", "threading",
            "generator", "iterator", "context manager"
        ]):
            return "hard"
        
        # Intermediate topics
        if any(word in title_lower for word in [
            "class", "module", "exception", "file", "package",
            "inheritance", "comprehension"
        ]):
            return "medium"
        
        # Early sections are usually beginner
        if order <= 5:
            return "easy"
        
        return "medium"


# ============================================================================
# Pre-configured scrapers
# ============================================================================

async def scrape_python_tutorial() -> List[Dict[str, Any]]:
    """
    Convenience function to scrape Python tutorial.
    
    Returns:
        List of scraped sections
    """
    async with PythonDocsScraper(version="3") as scraper:
        return await scraper.scrape_all()

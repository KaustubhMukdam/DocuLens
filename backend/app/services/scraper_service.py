# ============================================================================
# app/services/scraper_service.py
# ============================================================================
"""Service for orchestrating documentation scraping."""

from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.language import Language
from app.models.doc_section import DocSection, Difficulty
from app.models.code_example import CodeExample
from app.models.video_resource import VideoResource
from app.scrapers.python_docs import PythonDocsScraper
from app.scrapers.youtube import YouTubeIntegration
from app.services.ai_services import ai_service
from app.core.logging import logger


class ScraperService:
    """Service for scraping and storing documentation."""
    
    async def _get_or_create_language(
        self,
        db: AsyncSession,
        name: str,
        official_doc_url: str
    ) -> Language:
        """Get existing language or create new one."""
        # Check if exists
        result = await db.execute(
            select(Language).where(Language.name == name)
        )
        language = result.scalar_one_or_none()
        
        if language:
            logger.info(f"Language '{name}' already exists")
            return language
        
        # Create new
        language = Language(
            name=name,
            slug=name.lower(),
            description=f"Learn {name} programming",
            official_doc_url=official_doc_url,
            logo_url=f"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/{name.lower()}/{name.lower()}-original.svg"
        )
        db.add(language)
        await db.flush()
        
        logger.info(f"Created new language: {name}")
        return language
    
    async def _generate_summary(self, content: str) -> str:
        """Generate AI summary of content."""
        if not content or len(content) < 100:
            return "Introduction to programming concepts."
        
        try:
            # Limit content to first 3000 chars for summary
            truncated = content[:3000]
            
            # Use the correct method name from AIService
            summary = await ai_service.summarize_documentation(
                content=truncated,
                max_length=150,  # Max length in words
                style="concise",
                language_context="Python"
            )
            
            return summary if summary else "Learn programming fundamentals."
            
        except Exception as e:
            logger.error(f"Failed to generate AI summary: {e}")
            return "Comprehensive programming tutorial."
    
    async def scrape_and_store_language(
        self,
        db: AsyncSession,
        language_name: str,
        official_doc_url: str
    ) -> Dict[str, Any]:
        """
        Scrape a programming language documentation and store it.
        
        Args:
            db: Database session
            language_name: Name of the language (e.g., "Python")
            official_doc_url: Official documentation URL
            
        Returns:
            Summary of scraping results
        """
        logger.info(f"Starting scrape for {language_name}")
        
        # Get or create language
        language = await self._get_or_create_language(
            db, language_name, official_doc_url
        )
        
        # Choose appropriate scraper
        sections_data = []
        if language_name.lower() == "python":
            async with PythonDocsScraper() as scraper:
                sections_data = await scraper.scrape_all()
        else:
            raise ValueError(f"No scraper available for {language_name}")
        
        logger.info(f"Scraped {len(sections_data)} raw sections")
        
        # Store sections
        stored_count = 0
        total_sections = len(sections_data)
        
        for idx, section_data in enumerate(sections_data):
            try:
                # Validate section_data
                if not section_data:
                    logger.warning(f"Section {idx} returned None, skipping")
                    continue
                
                if "title" not in section_data:
                    logger.error(f"Section {idx} missing 'title' field. Keys: {list(section_data.keys())}")
                    continue
                
                if not section_data.get("content_raw"):
                    logger.warning(f"Section '{section_data.get('title')}' has no content, using placeholder")
                    section_data["content_raw"] = "Content will be available soon."
                
                # Generate AI summary
                content_preview = " ".join(section_data.get("content_raw", "").split()[:100])
                summary = await self._generate_summary(content_preview)
                
                # Determine path inclusion
                is_quick_path = idx < total_sections * 0.4  # Top 40%
                
                # Create section
                section = DocSection(
                    language_id=language.id,
                    title=section_data["title"],
                    slug=section_data["slug"],
                    content_raw=section_data.get("content_raw", "")[:50000],  # Limit size
                    content_summary=summary,
                    source_url=section_data["source_url"],
                    order_index=section_data["order_index"],
                    estimated_time_minutes=section_data.get("estimated_time_minutes", 30),
                    difficulty=Difficulty(section_data.get("difficulty", "medium")),
                    is_quick_path=is_quick_path,
                    is_deep_path=True
                )
                
                db.add(section)
                await db.flush()  # Get section ID
                
                # Add code examples individually (limit to 5 to prevent timeout)
                code_examples = section_data.get("code_examples", [])[:5]
                for code_data in code_examples:
                    try:
                        code_example = CodeExample(
                            doc_section_id=section.id,
                            **code_data
                        )
                        db.add(code_example)
                    except Exception as code_err:
                        logger.warning(f"Failed to add code example: {code_err}")
                        continue
                
                # COMMIT AFTER EACH SECTION to prevent connection timeout
                await db.commit()
                
                stored_count += 1
                logger.info(f"✓ Stored section {stored_count}/{total_sections}: {section.title}")
                
            except Exception as e:
                await db.rollback()  # Rollback this section's transaction
                logger.error(
                    f"✗ Error storing section '{section_data.get('title', 'Unknown')}': {e}",
                    exc_info=True
                )
                continue
        
        logger.info(f"Successfully stored {stored_count} sections for {language_name}")
        
        return {
            "language_id": str(language.id),
            "language_name": language_name,
            "sections_scraped": len(sections_data),
            "sections_stored": stored_count,
            "quick_path_sections": sum(1 for i in range(stored_count) if i < total_sections * 0.4),
        }
    
    async def add_videos_to_sections(
        self,
        db: AsyncSession,
        language_id: UUID,
        max_videos_per_section: int = 3
    ) -> int:
        """
        Add curated YouTube videos to documentation sections.
        
        Args:
            db: Database session
            language_id: Language ID
            max_videos_per_section: Maximum videos per section
            
        Returns:
            Total videos added
        """
        # Get all sections for this language
        result = await db.execute(
            select(DocSection).where(DocSection.language_id == language_id)
        )
        sections = result.scalars().all()
        
        if not sections:
            logger.warning(f"No sections found for language {language_id}")
            return 0
        
        youtube = YouTubeIntegration()
        total_videos = 0
        
        for section in sections:
            # Create search query from section title
            query = f"Python {section.title} tutorial"
            
            # Search for videos
            videos = await youtube.search_videos(
                query=query,
                max_results=max_videos_per_section
            )
            
            # Store videos
            for video_data in videos:
                video = VideoResource(
                    doc_section_id=section.id,
                    **video_data
                )
                db.add(video)
                total_videos += 1
        
        await db.commit()
        logger.info(f"Added {total_videos} videos to {len(sections)} sections")
        
        return total_videos


# ============================================================================
# Singleton instance
# ============================================================================

scraper_service = ScraperService()

# ============================================================================
# app/services/ai_service.py
# ============================================================================
"""AI service for content summarization and roadmap generation."""

from typing import Optional, Dict, Any, List
import asyncio
from datetime import datetime

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import BadRequestException, ServiceUnavailableException

# Groq client
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    logger.warning("Groq library not installed. AI features will be limited.")

# Anthropic client (fallback)
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("Anthropic library not installed. Fallback AI unavailable.")


class AIService:
    """AI service for summarization and content generation."""
    
    def __init__(self):
        """Initialize AI clients."""
        self.groq_client = None
        self.anthropic_client = None
        
        # Initialize Groq (primary)
        if GROQ_AVAILABLE and settings.GROQ_API_KEY:
            try:
                self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
                logger.info(f"Groq AI client initialized with model: {settings.GROQ_MODEL}")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
        
        # Initialize Anthropic (fallback)
        if ANTHROPIC_AVAILABLE and settings.ANTHROPIC_API_KEY:
            try:
                self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
                logger.info(f"Anthropic Claude client initialized with model: {settings.CLAUDE_MODEL}")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic client: {e}")
        
        if not self.groq_client and not self.anthropic_client:
            logger.warning("No AI clients available. AI features disabled.")
    
    async def summarize_documentation(
        self,
        content: str,
        max_length: int = 500,
        style: str = "concise",
        language_context: Optional[str] = None
    ) -> str:
        """Summarize documentation content using AI."""
        if not content or len(content.strip()) < 50:
            raise BadRequestException(
                message="Content too short to summarize",
                details={"min_length": 50}
            )
        
        # Truncate very long content
        max_input_chars = 50000
        if len(content) > max_input_chars:
            content = content[:max_input_chars] + "..."
            logger.warning(f"Content truncated to {max_input_chars} characters")
        
        system_prompt = self._build_summary_prompt(style, language_context)
        user_prompt = f"""Summarize the following documentation (max {max_length} words):

{content}

Provide a clear, accurate summary that preserves key technical details."""
        
        # Try Groq first
        if self.groq_client:
            try:
                summary = await self._summarize_with_groq(
                    system_prompt,
                    user_prompt,
                    max_tokens=max_length * 2
                )
                return summary
            except Exception as e:
                logger.error(f"Groq summarization failed: {e}")
        
        # Fallback to Claude
        if self.anthropic_client:
            try:
                summary = await self._summarize_with_claude(
                    system_prompt,
                    user_prompt,
                    max_tokens=max_length * 2
                )
                return summary
            except Exception as e:
                logger.error(f"Claude summarization failed: {e}")
        
        raise ServiceUnavailableException(
            message="AI summarization service temporarily unavailable",
            details={
                "groq_available": self.groq_client is not None,
                "claude_available": self.anthropic_client is not None
            }
        )
    
    async def generate_learning_roadmap(
        self,
        language_name: str,
        skill_level: str,
        available_hours_per_week: int,
        learning_goal: Optional[str] = None,
        path_type: str = "balanced"
    ) -> Dict[str, Any]:
        """Generate a personalized learning roadmap."""
        prompt = f"""Create a {path_type} learning roadmap for {language_name}.

User Profile:
- Skill Level: {skill_level}
- Available Time: {available_hours_per_week} hours/week
- Goal: {learning_goal or 'General proficiency'}

Generate a structured roadmap with:
1. Estimated total duration (weeks)
2. Weekly topics breakdown
3. Key concepts to master
4. Suggested practice frequency
5. Milestone checkpoints

Format as JSON."""
        
        if self.groq_client:
            try:
                roadmap = await self._generate_with_groq(prompt)
                return self._parse_roadmap_response(roadmap, available_hours_per_week)
            except Exception as e:
                logger.error(f"Groq roadmap generation failed: {e}")
        
        return self._generate_fallback_roadmap(
            language_name, skill_level, available_hours_per_week, path_type
        )
    
    def _build_summary_prompt(self, style: str, language_context: Optional[str]) -> str:
        """Build system prompt based on summary style."""
        base_prompt = "You are a technical documentation summarizer. "
        
        if language_context:
            base_prompt += f"You specialize in {language_context} documentation. "
        
        if style == "concise":
            base_prompt += "Create brief, clear summaries focusing on core concepts. "
        elif style == "detailed":
            base_prompt += "Create comprehensive summaries preserving technical details. "
        elif style == "bullet_points":
            base_prompt += "Create summaries as bullet points highlighting key points. "
        
        base_prompt += "Maintain accuracy and technical precision."
        return base_prompt
    
    async def _summarize_with_groq(
        self, system_prompt: str, user_prompt: str, max_tokens: int = 1000
    ) -> str:
        """Summarize using Groq API."""
        loop = asyncio.get_event_loop()
        
        def _call_groq():
            completion = self.groq_client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=settings.GROQ_TEMPERATURE,
                max_tokens=min(max_tokens, settings.GROQ_MAX_TOKENS),
                top_p=0.9,
            )
            return completion.choices[0].message.content
        
        return await loop.run_in_executor(None, _call_groq)
    
    async def _summarize_with_claude(
        self, system_prompt: str, user_prompt: str, max_tokens: int = 1000
    ) -> str:
        """Summarize using Anthropic Claude API."""
        loop = asyncio.get_event_loop()
        
        def _call_claude():
            message = self.anthropic_client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=min(max_tokens, settings.CLAUDE_MAX_TOKENS),
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                temperature=0.3,
            )
            return message.content[0].text
        
        return await loop.run_in_executor(None, _call_claude)
    
    async def _generate_with_groq(self, prompt: str) -> str:
        """Generate content using Groq."""
        loop = asyncio.get_event_loop()
        
        def _call_groq():
            completion = self.groq_client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=settings.GROQ_MAX_TOKENS,
            )
            return completion.choices[0].message.content
        
        return await loop.run_in_executor(None, _call_groq)
    
    def _parse_roadmap_response(self, response: str, hours_per_week: int) -> Dict[str, Any]:
        """Parse AI roadmap response."""
        import json
        
        try:
            data = json.loads(response)
            weeks = data.get("total_weeks", 8)
            completion_date = datetime.now() + timedelta(weeks=weeks)
            data["estimated_completion_date"] = completion_date.strftime("%Y-%m-%d")
            return data
        except:
            return self._generate_fallback_roadmap(
                "Unknown", "beginner", hours_per_week, "balanced"
            )
    
    def _generate_fallback_roadmap(
        self, language_name: str, skill_level: str,
        hours_per_week: int, path_type: str
    ) -> Dict[str, Any]:
        """Generate basic fallback roadmap."""
        from datetime import timedelta
        
        total_weeks = 8 if skill_level == "beginner" else 6
        if path_type == "quick":
            total_weeks = int(total_weeks * 0.6)
        elif path_type == "deep":
            total_weeks = int(total_weeks * 1.5)
        
        completion_date = datetime.now() + timedelta(weeks=total_weeks)
        
        return {
            "total_weeks": total_weeks,
            "weekly_schedule": [
                {
                    "week": i + 1,
                    "topics": [f"Week {i + 1} Core Concepts"],
                    "estimated_hours": hours_per_week,
                    "practice_recommendation": "Complete exercises and build small projects"
                }
                for i in range(total_weeks)
            ],
            "milestones": [
                f"Week {total_weeks // 3}: Basic Proficiency",
                f"Week {2 * total_weeks // 3}: Intermediate Skills",
                f"Week {total_weeks}: Project Completion"
            ],
            "estimated_completion_date": completion_date.strftime("%Y-%m-%d")
        }


# Global service instance
ai_service = AIService()

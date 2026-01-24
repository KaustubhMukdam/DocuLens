# backend/app/services/practice_service.py
"""Practice problem integration service."""
import logging
from typing import List, Dict, Optional
import httpx
from bs4 import BeautifulSoup
from app.models.practice_problem import PracticeProblem
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

logger = logging.getLogger(__name__)

class PracticeService:
    """Service for fetching practice problems."""
    
    async def search_leetcode_problems(
        self,
        topic: str,
        difficulty: str = "Easy",
        limit: int = 5
    ) -> List[Dict]:
        """Search LeetCode problems by topic."""
        try:
            # Use LeetCode GraphQL API
            url = "https://leetcode.com/graphql"
            
            query = """
            query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
              problemsetQuestionList: questionList(
                categorySlug: $categorySlug
                limit: $limit
                skip: $skip
                filters: $filters
              ) {
                questions: data {
                  questionId
                  title
                  titleSlug
                  difficulty
                  topicTags {
                    name
                    slug
                  }
                  stats
                }
              }
            }
            """
            
            variables = {
                "categorySlug": "",
                "skip": 0,
                "limit": limit,
                "filters": {
                    "difficulty": difficulty.upper(),
                    "tags": [topic.lower()]
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json={"query": query, "variables": variables},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    questions = data.get("data", {}).get("problemsetQuestionList", {}).get("questions", [])
                    
                    return [{
                        "title": q["title"],
                        "url": f"https://leetcode.com/problems/{q['titleSlug']}/",
                        "difficulty": q["difficulty"],
                        "problem_id": q["questionId"],
                        "topics": [tag["name"] for tag in q.get("topicTags", [])]
                    } for q in questions]
                    
        except Exception as e:
            logger.error(f"Error fetching LeetCode problems: {e}")
        
        return []
    
    async def scrape_problems_for_section(
        self,
        db: AsyncSession,
        section_id: UUID,
        section_title: str,
        difficulty: str = "Easy"
    ) -> List[PracticeProblem]:
        """Scrape and save practice problems for a section."""
        # Extract main topic from section title
        topic = section_title.split()[0].lower()  # Simple extraction
        
        problems_data = await self.search_leetcode_problems(
            topic=topic,
            difficulty=difficulty,
            limit=3
        )
        
        practice_problems = []
        for prob in problems_data:
            problem = PracticeProblem(
                doc_section_id=section_id,
                title=prob["title"],
                url=prob["url"],
                difficulty=prob["difficulty"].lower(),
                source="leetcode",
                problem_id=prob["problem_id"]
            )
            db.add(problem)
            practice_problems.append(problem)
        
        await db.commit()
        return practice_problems


practice_service = PracticeService()

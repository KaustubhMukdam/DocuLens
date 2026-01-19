# ============================================================================
# app/scrapers/leetcode.py
# ============================================================================
"""LeetCode problem scraper and matcher."""

from typing import List, Dict, Any, Optional
import httpx
import re

from app.core.logging import logger


class LeetCodeScraper:
    """
    LeetCode problem scraper.
    
    Note: LeetCode has rate limiting. Use sparingly or with API access.
    """
    
    def __init__(self):
        """Initialize LeetCode scraper."""
        self.base_url = "https://leetcode.com"
        self.graphql_url = f"{self.base_url}/graphql"
    
    async def search_problems_by_topic(
        self,
        topic: str,
        difficulty: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for LeetCode problems by topic.
        
        Args:
            topic: Topic/tag to search for (e.g., "array", "string")
            difficulty: Optional difficulty filter (easy, medium, hard)
            limit: Maximum number of problems
            
        Returns:
            List of problem metadata
        """
        try:
            # Use LeetCode's GraphQL API
            query = """
            query problemsetQuestionList($categorySlug: String, $limit: Int, $filters: QuestionListFilterInput) {
              problemsetQuestionList: questionList(
                categorySlug: $categorySlug
                limit: $limit
                filters: $filters
              ) {
                questions: data {
                  questionId
                  questionFrontendId
                  title
                  titleSlug
                  difficulty
                  topicTags {
                    name
                    slug
                  }
                  acRate
                }
              }
            }
            """
            
            variables = {
                "categorySlug": "",
                "limit": limit,
                "filters": {
                    "tags": [topic.lower()]
                }
            }
            
            if difficulty:
                variables["filters"]["difficulty"] = difficulty.upper()
            
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.graphql_url,
                    json={"query": query, "variables": variables},
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    logger.warning(f"LeetCode API returned {response.status_code}")
                    return self._get_fallback_problems(topic, difficulty, limit)
                
                data = response.json()
                problems = data.get("data", {}).get("problemsetQuestionList", {}).get("questions", [])
                
                return self._format_problems(problems)
                
        except Exception as e:
            logger.error(f"LeetCode scraping error: {e}")
            return self._get_fallback_problems(topic, difficulty, limit)
    
    def _format_problems(self, problems: List[Dict]) -> List[Dict[str, Any]]:
        """Format LeetCode problems for storage."""
        formatted = []
        
        for idx, problem in enumerate(problems):
            title_slug = problem.get("titleSlug", "")
            problem_url = f"{self.base_url}/problems/{title_slug}/"
            
            # Extract tags
            tags = [tag["name"] for tag in problem.get("topicTags", [])]
            
            formatted.append({
                "title": problem.get("title", ""),
                "platform": "leetcode",
                "difficulty": problem.get("difficulty", "Medium").lower(),
                "problem_url": problem_url,
                "description": f"LeetCode #{problem.get('questionFrontendId')} - Acceptance: {problem.get('acRate', 0):.1f}%",
                "tags": tags[:5],  # Limit tags
                "order_index": idx
            })
        
        return formatted
    
    def _get_fallback_problems(
        self,
        topic: str,
        difficulty: Optional[str],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Fallback: Return curated problem recommendations.
        
        Used when API is unavailable or rate-limited.
        """
        # Curated problems by topic
        curated_problems = {
            "array": [
                {"id": "1", "title": "Two Sum", "difficulty": "easy"},
                {"id": "15", "title": "3Sum", "difficulty": "medium"},
                {"id": "53", "title": "Maximum Subarray", "difficulty": "medium"},
                {"id": "121", "title": "Best Time to Buy and Sell Stock", "difficulty": "easy"},
            ],
            "string": [
                {"id": "3", "title": "Longest Substring Without Repeating Characters", "difficulty": "medium"},
                {"id": "5", "title": "Longest Palindromic Substring", "difficulty": "medium"},
                {"id": "20", "title": "Valid Parentheses", "difficulty": "easy"},
            ],
            "tree": [
                {"id": "94", "title": "Binary Tree Inorder Traversal", "difficulty": "easy"},
                {"id": "102", "title": "Binary Tree Level Order Traversal", "difficulty": "medium"},
                {"id": "104", "title": "Maximum Depth of Binary Tree", "difficulty": "easy"},
            ],
            "dynamic-programming": [
                {"id": "70", "title": "Climbing Stairs", "difficulty": "easy"},
                {"id": "198", "title": "House Robber", "difficulty": "medium"},
                {"id": "322", "title": "Coin Change", "difficulty": "medium"},
            ]
        }
        
        topic_key = topic.lower().replace(" ", "-")
        problems = curated_problems.get(topic_key, curated_problems["array"])
        
        # Filter by difficulty if specified
        if difficulty:
            problems = [p for p in problems if p["difficulty"] == difficulty.lower()]
        
        # Format and limit
        formatted = []
        for idx, problem in enumerate(problems[:limit]):
            formatted.append({
                "title": problem["title"],
                "platform": "leetcode",
                "difficulty": problem["difficulty"],
                "problem_url": f"{self.base_url}/problems/{problem['title'].lower().replace(' ', '-')}/",
                "description": f"LeetCode #{problem['id']}",
                "tags": [topic],
                "order_index": idx
            })
        
        return formatted


# ============================================================================
# Topic mapping helper
# ============================================================================

LEETCODE_TOPIC_MAPPING = {
    # Python concepts -> LeetCode tags
    "lists": "array",
    "strings": "string",
    "dictionaries": "hash-table",
    "sets": "hash-table",
    "functions": "design",
    "classes": "design",
    "recursion": "recursion",
    "sorting": "sorting",
    "searching": "binary-search",
    "trees": "tree",
    "graphs": "graph",
    "dynamic programming": "dynamic-programming",
}


async def get_problems_for_topic(
    topic: str,
    difficulty: Optional[str] = None,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Get LeetCode problems for a documentation topic.
    
    Args:
        topic: Topic name from documentation
        difficulty: Optional difficulty filter
        limit: Maximum number of problems
        
    Returns:
        List of problem metadata
    """
    # Map topic to LeetCode tag
    topic_lower = topic.lower()
    leetcode_tag = LEETCODE_TOPIC_MAPPING.get(topic_lower, topic_lower)
    
    scraper = LeetCodeScraper()
    return await scraper.search_problems_by_topic(
        topic=leetcode_tag,
        difficulty=difficulty,
        limit=limit
    )

# ============================================================================
# app/scrapers/youtube.py
# ============================================================================
"""YouTube video integration for curated tutorials."""

from typing import List, Dict, Any, Optional
import httpx
from datetime import timedelta

from app.core.config import settings
from app.core.logging import logger


class YouTubeIntegration:
    """Integration with YouTube Data API v3."""
    
    def __init__(self):
        """Initialize YouTube integration."""
        self.api_key = settings.YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    async def search_videos(
        self,
        query: str,
        max_results: int = 5,
        order: str = "relevance"
    ) -> List[Dict[str, Any]]:
        """
        Search for videos on YouTube.
        
        Args:
            query: Search query (e.g., "Python tutorial")
            max_results: Maximum number of results
            order: Sort order (relevance, date, viewCount, rating)
            
        Returns:
            List of video metadata
        """
        if not self.api_key:
            logger.warning("YouTube API key not configured")
            return []
        
        url = f"{self.base_url}/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "order": order,
            "videoDuration": "medium",  # 4-20 minutes
            "videoDefinition": "high",
            "relevanceLanguage": "en",
            "key": self.api_key
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
            
            videos = []
            video_ids = [item["id"]["videoId"] for item in data.get("items", [])]
            
            # Get detailed video info
            if video_ids:
                details = await self._get_video_details(video_ids)
                videos = self._format_videos(data.get("items", []), details)
            
            logger.info(f"Found {len(videos)} videos for query: {query}")
            return videos
            
        except Exception as e:
            logger.error(f"YouTube search error: {e}")
            return []
    
    async def _get_video_details(self, video_ids: List[str]) -> Dict[str, Any]:
        """Get detailed information for videos."""
        url = f"{self.base_url}/videos"
        params = {
            "part": "contentDetails,statistics",
            "id": ",".join(video_ids),
            "key": self.api_key
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
            
            # Create lookup dict
            return {
                item["id"]: item
                for item in data.get("items", [])
            }
        except Exception as e:
            logger.error(f"Error fetching video details: {e}")
            return {}
    
    def _format_videos(
        self,
        search_items: List[Dict],
        details: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Format video data for storage."""
        formatted = []
        
        for idx, item in enumerate(search_items):
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]
            detail = details.get(video_id, {})
            
            # Parse duration
            duration_seconds = None
            if detail:
                duration_iso = detail.get("contentDetails", {}).get("duration")
                if duration_iso:
                    duration_seconds = self._parse_duration(duration_iso)
            
            # Get view count
            views = None
            if detail:
                view_count = detail.get("statistics", {}).get("viewCount")
                if view_count:
                    views = int(view_count)
            
            formatted.append({
                "title": snippet.get("title", ""),
                "video_url": f"https://www.youtube.com/watch?v={video_id}",  # Changed from 'url'
                "platform": "youtube",
                "channel_name": snippet.get("channelTitle", ""),
                "thumbnail_url": snippet.get("thumbnails", {}).get("high", {}).get("url"),
                "duration_seconds": duration_seconds,
                "views": views
            })
        
        return formatted
    
    def _parse_duration(self, duration_iso: str) -> int:
        """
        Parse ISO 8601 duration to seconds.
        
        Args:
            duration_iso: ISO duration string (e.g., "PT15M33S")
            
        Returns:
            Duration in seconds
        """
        import re
        
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_iso)
        
        if not match:
            return 0
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds


# ============================================================================
# Convenience functions
# ============================================================================

async def search_tutorial_videos(topic: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for tutorial videos on a topic.
    
    Args:
        topic: Topic to search for
        max_results: Maximum number of results
        
    Returns:
        List of video metadata
    """
    youtube = YouTubeIntegration()
    query = f"{topic} tutorial programming"
    return await youtube.search_videos(query, max_results=max_results)

# backend/app/services/video_service.py
"""Enhanced video scraping and management service."""
import logging
from typing import List, Optional, Dict
import httpx
from app.core.config import settings
from app.models.video_resource import VideoResource
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

logger = logging.getLogger(__name__)

class VideoService:
    """Service for managing video resources."""
    
    def __init__(self):
        self.youtube_api_key = settings.YOUTUBE_API_KEY
        self.youtube_base_url = "https://www.googleapis.com/youtube/v3"
    
    async def search_videos(
        self,
        query: str,
        max_results: int = 5,
        language: str = "en"
    ) -> List[Dict]:
        """Search YouTube for relevant videos."""
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "maxResults": max_results,
                    "key": self.youtube_api_key,
                    "relevanceLanguage": language,
                    "videoEmbeddable": "true",
                    "videoDuration": "medium",  # 4-20 minutes
                    "order": "relevance"
                }
                
                response = await client.get(
                    f"{self.youtube_base_url}/search",
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                videos = []
                for item in data.get("items", []):
                    video_id = item["id"]["videoId"]
                    snippet = item["snippet"]
                    
                    # Get video statistics
                    stats = await self._get_video_stats(video_id)
                    
                    videos.append({
                        "video_id": video_id,
                        "title": snippet["title"],
                        "description": snippet["description"],
                        "thumbnail_url": snippet["thumbnails"]["high"]["url"],
                        "channel_name": snippet["channelTitle"],
                        "published_at": snippet["publishedAt"],
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "view_count": stats.get("viewCount", 0),
                        "like_count": stats.get("likeCount", 0),
                        "duration": stats.get("duration", "")
                    })
                
                return videos
                
        except Exception as e:
            logger.error(f"Error searching YouTube videos: {e}")
            return []
    
    async def _get_video_stats(self, video_id: str) -> Dict:
        """Get video statistics."""
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "part": "statistics,contentDetails",
                    "id": video_id,
                    "key": self.youtube_api_key
                }
                
                response = await client.get(
                    f"{self.youtube_base_url}/videos",
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                if not data.get("items"):
                    return {}
                
                item = data["items"][0]
                stats = item.get("statistics", {})
                content = item.get("contentDetails", {})
                
                return {
                    "viewCount": int(stats.get("viewCount", 0)),
                    "likeCount": int(stats.get("likeCount", 0)),
                    "duration": content.get("duration", "")
                }
        except Exception as e:
            logger.error(f"Error getting video stats: {e}")
            return {}
    
    async def scrape_videos_for_section(
        self,
        db: AsyncSession,
        section_id: UUID,
        section_title: str,
        language_name: str
    ) -> List[VideoResource]:
        """Scrape and save videos for a documentation section."""
        query = f"{language_name} {section_title} tutorial programming"
        videos = await self.search_videos(query, max_results=3)
        
        video_resources = []
        for video in videos:
            video_resource = VideoResource(
                doc_section_id=section_id,
                title=video["title"],
                url=video["url"],
                thumbnail_url=video["thumbnail_url"],
                duration_minutes=self._parse_duration(video["duration"]),
                source="youtube",
                channel_name=video["channel_name"]
            )
            db.add(video_resource)
            video_resources.append(video_resource)
        
        await db.commit()
        return video_resources
    
    def _parse_duration(self, duration_iso: str) -> int:
        """Parse ISO 8601 duration to minutes."""
        try:
            import isodate
            duration = isodate.parse_duration(duration_iso)
            return int(duration.total_seconds() / 60)
        except:
            return 10  # Default 10 minutes


# Initialize service
video_service = VideoService()

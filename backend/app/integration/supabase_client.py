"""
Supabase storage client for file uploads.
"""

from typing import Optional
from supabase import create_client, Client
from app.core.config import settings
from loguru import logger


class SupabaseStorage:
    """Supabase storage client."""
    
    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY
        )
        self.bucket = settings.SUPABASE_BUCKET
    
    async def upload_file(
        self,
        file_path: str,
        file_data: bytes,
        content_type: str = "application/octet-stream"
    ) -> str:
        """
        Upload file to Supabase storage.
        
        Args:
            file_path: Path in bucket (e.g., 'avatars/user123.png')
            file_data: File content as bytes
            content_type: MIME type
            
        Returns:
            Public URL of uploaded file
        """
        try:
            response = self.client.storage.from_(self.bucket).upload(
                path=file_path,
                file=file_data,
                file_options={"content-type": content_type}
            )
            
            # Get public URL
            public_url = self.client.storage.from_(self.bucket).get_public_url(file_path)
            
            logger.info(f"Uploaded file to Supabase: {file_path}")
            return public_url
            
        except Exception as e:
            logger.error(f"Failed to upload to Supabase: {e}")
            raise
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete file from storage."""
        try:
            self.client.storage.from_(self.bucket).remove([file_path])
            logger.info(f"Deleted file from Supabase: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete from Supabase: {e}")
            return False


# Global instance
supabase_storage = SupabaseStorage()
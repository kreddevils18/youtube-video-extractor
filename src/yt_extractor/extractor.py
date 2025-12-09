"""YouTube video extraction logic."""

import ssl
from typing import Any
import certifi
import yt_dlp
from .config import YT_DLP_OPTIONS



class VideoExtractor:
    """Extracts video metadata from YouTube channels."""
    
    def __init__(self, channel_url: str) -> None:
        """Initialize the extractor with a channel URL.
        
        Args:
            channel_url: The YouTube channel URL to extract videos from
        """
        self.channel_url = channel_url
        self._videos: list[dict[str, Any]] = []
        self._channel_name: str = ""
    
    def extract(self) -> tuple[list[dict[str, Any]], str]:
        """Extract all videos from the channel.
        
        Returns:
            A tuple of (videos list, channel name)
            Each video is a dict with keys: id, title, description, url, upload_date
            
        Raises:
            Exception: If extraction fails
        """
        try:
            # Create SSL context with certifi certificates
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            
            # Merge SSL context into options
            # Use extract_flat='in_playlist' to get video IDs without full metadata
            options = {
                **YT_DLP_OPTIONS,
                "ssl_context": ssl_context,
                "extract_flat": "in_playlist",  # Get video entries without downloading full metadata
            }
            
            with yt_dlp.YoutubeDL(options) as ydl:
                # Extract channel information
                info = ydl.extract_info(self.channel_url, download=False)
                
                if not info:
                    raise ValueError("Could not extract channel information")
                
                # Get channel name
                self._channel_name = info.get("channel", info.get("uploader", "unknown"))
                
                # Get all video entries
                entries = info.get("entries", [])
                
                # If entries are playlists (Videos, Shorts, Live), flatten them
                all_videos = []
                for entry in entries:
                    if not entry:
                        continue
                    
                    # Check if this is a playlist/tab
                    if entry.get("_type") == "playlist":
                        # Get videos from this playlist
                        sub_entries = entry.get("entries", [])
                        all_videos.extend([e for e in sub_entries if e])
                    else:
                        # This is a direct video entry
                        all_videos.append(entry)
                
                # Extract relevant video information
                self._videos = []
                for entry in all_videos:
                    video_id = entry.get("id", "")
                    if not video_id:
                        continue
                    
                    video_data = {
                        "id": video_id,
                        "title": entry.get("title", ""),
                        "description": entry.get("description", ""),
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "upload_date": entry.get("upload_date", entry.get("release_timestamp", "")),
                    }
                    self._videos.append(video_data)
                
                return self._videos, self._channel_name
                
        except Exception as e:
            raise Exception(f"Failed to extract videos: {str(e)}") from e
    
    @property
    def videos(self) -> list[dict[str, Any]]:
        """Get the extracted videos."""
        return self._videos
    
    @property
    def channel_name(self) -> str:
        """Get the channel name."""
        return self._channel_name

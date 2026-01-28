"""YouTube API Client wrapper."""
from googleapiclient.discovery import build
from typing import Optional


class YouTubeClient:
    """Wrapper for YouTube Data API v3."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._client: Optional["build"] = None

    @property
    def client(self):
        """Lazy-load the YouTube API client."""
        if self._client is None:
            self._client = build("youtube", "v3", developerKey=self.api_key)
        return self._client

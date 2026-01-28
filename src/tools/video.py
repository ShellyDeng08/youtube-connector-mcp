"""YouTube Video Details Tool."""
from typing import Optional, List
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class GetVideoArgs(BaseModel):
    """Arguments for getting video details."""
    video_id: str = Field(description="YouTube video ID (11 characters)")
    part: List[str] = Field(
        default=["snippet", "statistics", "contentDetails"],
        description="Parts to retrieve: snippet, statistics, contentDetails"
    )


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_get_video(video_id: str, part: list = None):
    """Get detailed information about a YouTube video.

    Args:
        video_id: 11-character YouTube video ID
        part: List of parts to retrieve

    Returns:
        Dictionary with video details or error
    """
    if part is None:
        part = ["snippet", "statistics", "contentDetails"]

    client = _get_client()

    try:
        response = client.client.videos().list(
            id=video_id,
            part=",".join(part)
        ).execute()

        if not response.get("items"):
            return {
                "data": None,
                "error": {
                    "code": "NotFound",
                    "message": f"Video not found: {video_id}"
                },
                "pagination": None
            }

        return {
            "data": response["items"][0],
            "error": None,
            "pagination": None
        }
    except Exception as e:
        return {
            "data": None,
            "error": {"code": type(e).__name__, "message": str(e)},
            "pagination": None
        }


def register_video_tools(server):
    """Register video tools with MCP server."""
    @server.call_tool()
    async def call_youtube_get_video(name, arguments):
        if name != "youtube_get_video":
            return None

        args = GetVideoArgs(**arguments)
        return await youtube_get_video(
            video_id=args.video_id,
            part=args.part
        )

    @server.list_tools()
    async def list_video_tools():
        return [{
            "name": "youtube_get_video",
            "description": "Get detailed information about a YouTube video",
            "inputSchema": GetVideoArgs.model_json_schema()
        }]

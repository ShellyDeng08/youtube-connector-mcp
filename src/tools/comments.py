"""YouTube Comments Tool."""
from typing import Optional
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class GetCommentsArgs(BaseModel):
    """Arguments for getting comments."""
    video_id: str = Field(description="YouTube video ID")
    max_results: int = Field(default=20, description="Maximum comments (1-100)")
    page_token: Optional[str] = Field(default=None, description="Page token for pagination")


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_get_comments(video_id: str, max_results: int = 20, page_token: str = None):
    """Get comments for a YouTube video.

    Args:
        video_id: 11-character YouTube video ID
        max_results: Maximum comments (1-100)
        page_token: Pagination token for next page

    Returns:
        Dictionary with comments or error
    """
    client = _get_client()

    try:
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": min(max_results, 100),
            "order": "relevance"
        }

        if page_token:
            params["pageToken"] = page_token

        response = client.client.commentThreads().list(**params).execute()

        return {
            "data": response.get("items", []),
            "error": None,
            "pagination": {
                "nextPageToken": response.get("nextPageToken"),
                "totalResults": response.get("pageInfo", {}).get("totalResults", 0)
            }
        }
    except Exception as e:
        return {
            "data": None,
            "error": {"code": type(e).__name__, "message": str(e)},
            "pagination": None
        }


def register_comments_tools(server):
    """Register comments tools with MCP server."""
    @server.call_tool()
    async def call_youtube_get_comments(name, arguments):
        if name != "youtube_get_comments":
            return None

        args = GetCommentsArgs(**arguments)
        return await youtube_get_comments(
            video_id=args.video_id,
            max_results=args.max_results,
            page_token=args.page_token
        )

    @server.list_tools()
    async def list_comments_tools():
        return [{
            "name": "youtube_get_comments",
            "description": "Get comments for a YouTube video",
            "inputSchema": GetCommentsArgs.model_json_schema()
        }]

"""YouTube Analytics Tool."""
from typing import Optional, List
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class GetAnalyticsArgs(BaseModel):
    """Arguments for getting analytics."""
    ids: str = Field(description="Channel or video ID (format: channel==ID or video==ID)")
    metrics: List[str] = Field(
        default=["views", "likes", "comments"],
        description="Metrics to retrieve: views, likes, comments, dislikes, estimatedMinutesWatched"
    )
    start_date: Optional[str] = Field(default=None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(default=None, description="End date (YYYY-MM-DD)")


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_get_analytics(ids: str, metrics: list = None, start_date: str = None, end_date: str = None):
    """Get analytics data for a channel or video.

    Note: This requires additional OAuth scopes. With API key only, limited data is available.
    Basic statistics are available via videos/channels endpoints.

    Args:
        ids: Channel or video ID (format: channel==ID or video==ID)
        metrics: List of metrics to retrieve
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)

    Returns:
        Dictionary with analytics data or error
    """
    if metrics is None:
        metrics = ["views", "likes", "comments"]

    # With API key only, we can only return basic statistics from videos/channels endpoints
    # Full analytics requires OAuth authentication

    return {
        "data": {
            "message": "Full analytics API requires OAuth authentication. "
                      "With API key only, use youtube_get_video or youtube_get_channel "
                      "for basic statistics (views, likes, comments)."
        },
        "error": {
            "code": "AuthRequired",
            "message": "Analytics API requires OAuth scope. Use youtube_get_video/channel for basic stats."
        },
        "pagination": None
    }


def register_analytics_tools(server):
    """Register analytics tools with MCP server."""
    @server.call_tool()
    async def call_youtube_get_analytics(name, arguments):
        if name != "youtube_get_analytics":
            return None

        args = GetAnalyticsArgs(**arguments)
        return await youtube_get_analytics(
            ids=args.ids,
            metrics=args.metrics,
            start_date=args.start_date,
            end_date=args.end_date
        )

    @server.list_tools()
    async def list_analytics_tools():
        return [{
            "name": "youtube_get_analytics",
            "description": "Get analytics data (requires OAuth for full data, API key provides basic stats via video/channel tools)",
            "inputSchema": GetAnalyticsArgs.model_json_schema()
        }]

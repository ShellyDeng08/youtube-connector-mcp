"""YouTube Search Tool."""
from typing import Optional
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class SearchArgs(BaseModel):
    """Arguments for YouTube search."""
    query: str = Field(description="Search query")
    max_results: int = Field(default=10, description="Maximum results (1-50)")
    order: str = Field(
        default="relevance",
        description="Order: relevance, date, viewCount, rating"
    )
    type: str = Field(
        default="video",
        description="Resource type: video, channel, playlist"
    )


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_search(query: str, max_results: int = 10, order: str = "relevance", type: str = "video"):
    """Search YouTube for videos, channels, or playlists.

    Args:
        query: Search terms
        max_results: Number of results (1-50)
        order: Sort order (relevance, date, viewCount, rating)
        type: Resource type (video, channel, playlist)

    Returns:
        Dictionary with search results or error
    """
    client = _get_client()

    search_params = {
        "q": query,
        "maxResults": min(max_results, 50),
        "order": order,
        "type": type,
        "part": "id,snippet"
    }

    try:
        response = client.client.search().list(**search_params).execute()
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
            "error": {"code": e.__class__.__name__, "message": str(e)},
            "pagination": None
        }


def register_search_tools(server):
    """Register search tools with MCP server."""
    @server.call_tool()
    async def call_youtube_search(name, arguments):
        if name != "youtube_search":
            return None

        args = SearchArgs(**arguments)
        return await youtube_search(
            query=args.query,
            max_results=args.max_results,
            order=args.order,
            type=args.type
        )

    @server.list_tools()
    async def list_search_tools():
        return [{
            "name": "youtube_search",
            "description": "Search YouTube for videos, channels, or playlists",
            "inputSchema": SearchArgs.model_json_schema()
        }]

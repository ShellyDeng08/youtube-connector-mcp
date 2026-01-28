"""YouTube Channel Tool."""
from typing import Optional
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class GetChannelArgs(BaseModel):
    """Arguments for getting channel details."""
    channel_id: Optional[str] = Field(default=None, description="YouTube channel ID")
    username: Optional[str] = Field(default=None, description="Channel username (e.g., @channel)")


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_get_channel(channel_id: str = None, username: str = None):
    """Get channel information.

    Args:
        channel_id: YouTube channel ID (24 characters)
        username: Channel username starting with @

    Returns:
        Dictionary with channel data or error
    """
    client = _get_client()

    if not channel_id and not username:
        return {
            "data": None,
            "error": {
                "code": "InvalidInput",
                "message": "Either channel_id or username is required"
            },
            "pagination": None
        }

    try:
        params = {
            "part": "snippet,statistics,contentDetails"
        }

        if username:
            # Convert username to channel ID
            # For API v3, we use 'forUsername' parameter
            params["forUsername"] = username.lstrip("@")
        else:
            params["id"] = channel_id

        response = client.client.channels().list(**params).execute()

        if not response.get("items"):
            return {
                "data": None,
                "error": {
                    "code": "NotFound",
                    "message": f"Channel not found: {channel_id or username}"
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


def register_channel_tools(server):
    """Register channel tools with MCP server."""
    @server.call_tool()
    async def call_youtube_get_channel(name, arguments):
        if name != "youtube_get_channel":
            return None

        args = GetChannelArgs(**arguments)
        return await youtube_get_channel(
            channel_id=args.channel_id,
            username=args.username
        )

    @server.list_tools()
    async def list_channel_tools():
        return [{
            "name": "youtube_get_channel",
            "description": "Get channel information",
            "inputSchema": GetChannelArgs.model_json_schema()
        }]

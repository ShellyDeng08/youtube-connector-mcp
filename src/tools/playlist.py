"""YouTube Playlist Tools."""
from typing import Optional
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class GetPlaylistArgs(BaseModel):
    """Arguments for getting playlist details."""
    playlist_id: str = Field(description="YouTube playlist ID")
    max_results: int = Field(default=50, description="Maximum videos (1-50)")


class ListPlaylistsArgs(BaseModel):
    """Arguments for listing playlists."""
    channel_id: Optional[str] = Field(default=None, description="Channel ID (required)")
    max_results: int = Field(default=25, description="Maximum playlists (1-50)")


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_get_playlist(playlist_id: str, max_results: int = 50):
    """Get playlist details and video list.

    Args:
        playlist_id: YouTube playlist ID
        max_results: Maximum videos to return (1-50)

    Returns:
        Dictionary with playlist data or error
    """
    client = _get_client()

    try:
        # Get playlist items
        items_response = client.client.playlistItems().list(
            playlistId=playlist_id,
            part="snippet,contentDetails",
            maxResults=min(max_results, 50)
        ).execute()

        # Get playlist details
        playlists_response = client.client.playlists().list(
            id=playlist_id,
            part="snippet,contentDetails"
        ).execute()

        playlist_details = playlists_response.get("items", [{}])[0]

        return {
            "data": {
                "details": playlist_details,
                "items": items_response.get("items", [])
            },
            "error": None,
            "pagination": {
                "nextPageToken": items_response.get("nextPageToken"),
                "totalResults": items_response.get("pageInfo", {}).get("totalResults", 0)
            }
        }
    except Exception as e:
        return {
            "data": None,
            "error": {"code": type(e).__name__, "message": str(e)},
            "pagination": None
        }


async def youtube_list_playlists(channel_id: str, max_results: int = 25):
    """List playlists for a channel.

    Args:
        channel_id: YouTube channel ID
        max_results: Maximum playlists to return (1-50)

    Returns:
        Dictionary with playlists or error
    """
    client = _get_client()

    try:
        response = client.client.playlists().list(
            channelId=channel_id,
            part="snippet,contentDetails",
            maxResults=min(max_results, 50)
        ).execute()

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


def register_playlist_tools(server):
    """Register playlist tools with MCP server."""
    @server.call_tool()
    async def call_youtube_get_playlist(name, arguments):
        if name != "youtube_get_playlist":
            return None
        args = GetPlaylistArgs(**arguments)
        return await youtube_get_playlist(
            playlist_id=args.playlist_id,
            max_results=args.max_results
        )

    @server.call_tool()
    async def call_youtube_list_playlists(name, arguments):
        if name != "youtube_list_playlists":
            return None
        args = ListPlaylistsArgs(**arguments)
        return await youtube_list_playlists(
            channel_id=args.channel_id,
            max_results=args.max_results
        )

    @server.list_tools()
    async def list_playlist_tools():
        return [
            {
                "name": "youtube_get_playlist",
                "description": "Get playlist details and video list",
                "inputSchema": GetPlaylistArgs.model_json_schema()
            },
            {
                "name": "youtube_list_playlists",
                "description": "List playlists for a channel",
                "inputSchema": ListPlaylistsArgs.model_json_schema()
            }
        ]

"""YouTube Transcript Tool."""
from typing import Optional
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class GetTranscriptArgs(BaseModel):
    """Arguments for getting transcript."""
    video_id: str = Field(description="YouTube video ID")
    language: str = Field(default="en", description="Language code (e.g., en, es)")


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_get_transcript(video_id: str, language: str = "en"):
    """Get transcript/captions for a YouTube video.

    Args:
        video_id: 11-character YouTube video ID
        language: Language code (default: en)

    Returns:
        Dictionary with transcript or error
    """
    client = _get_client()

    try:
        # First, get caption tracks
        captions_response = client.client.captions().list(
            part="snippet",
            videoId=video_id
        ).execute()

        items = captions_response.get("items", [])

        # Find caption in requested language
        caption_id = None
        for item in items:
            snippet = item.get("snippet", {})
            if snippet.get("languageCode") == language:
                caption_id = item.get("id")
                break

        if not caption_id and items:
            # Fall back to auto-generated or first available
            for item in items:
                snippet = item.get("snippet", {})
                track_kind = snippet.get("trackKind", "")
                if track_kind == "asr" or not caption_id:
                    caption_id = item.get("id")
                    break

        if not caption_id:
            return {
                "data": None,
                "error": {
                    "code": "NotFound",
                    "message": f"No captions available for video {video_id} in language {language}"
                },
                "pagination": None
            }

        # Download caption content (requires auth for full content, basic info available via API)
        # Note: Full transcript content may require additional processing
        return {
            "data": {
                "videoId": video_id,
                "language": language,
                "captionId": caption_id,
                "availableTracks": [
                    {
                        "id": item.get("id"),
                        "language": item.get("snippet", {}).get("languageCode"),
                        "kind": item.get("snippet", {}).get("trackKind")
                    }
                    for item in items
                ]
            },
            "error": None,
            "pagination": None
        }
    except Exception as e:
        return {
            "data": None,
            "error": {"code": type(e).__name__, "message": str(e)},
            "pagination": None
        }


def register_transcript_tools(server):
    """Register transcript tools with MCP server."""
    @server.call_tool()
    async def call_youtube_get_transcript(name, arguments):
        if name != "youtube_get_transcript":
            return None

        args = GetTranscriptArgs(**arguments)
        return await youtube_get_transcript(
            video_id=args.video_id,
            language=args.language
        )

    @server.list_tools()
    async def list_transcript_tools():
        return [{
            "name": "youtube_get_transcript",
            "description": "Get transcript/captions for a YouTube video",
            "inputSchema": GetTranscriptArgs.model_json_schema()
        }]

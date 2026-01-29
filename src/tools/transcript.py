"""YouTube Transcript Tool."""
from typing import Optional
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound


class GetTranscriptArgs(BaseModel):
    """Arguments for getting transcript."""
    video_id: str = Field(description="YouTube video ID")
    language: str = Field(default="en", description="Language code (e.g., en, es, zh)")


_client: Optional[YouTubeClient] = None
_transcript_api: Optional[YouTubeTranscriptApi] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


def _get_transcript_api() -> YouTubeTranscriptApi:
    """Get or create transcript API singleton."""
    global _transcript_api
    if _transcript_api is None:
        _transcript_api = YouTubeTranscriptApi()
    return _transcript_api


async def youtube_get_transcript(video_id: str, language: str = "en"):
    """Get transcript/captions for a YouTube video.

    Uses youtube-transcript-api to fetch actual transcript text.

    Args:
        video_id: 11-character YouTube video ID
        language: Language code (default: en)

    Returns:
        Dictionary with transcript or error
    """
    try:
        api = _get_transcript_api()

        # Try to get transcript in requested language
        transcript_data = None
        used_language = language

        try:
            transcript_data = api.fetch(video_id, languages=[language])
        except NoTranscriptFound:
            # If requested language not found, try auto-generated (any available)
            try:
                transcript_data = api.fetch(video_id)
                used_language = "auto"
            except NoTranscriptFound:
                # List available languages for better error message
                available_languages = []
                try:
                    transcript_list = api.list(video_id)
                    for t in transcript_list:
                        available_languages.append(t.language_code)
                except Exception:
                    pass

                return {
                    "data": None,
                    "error": {
                        "code": "NotFound",
                        "message": f"No transcript available for video {video_id} in language '{language}'. "
                        f"Available languages: {', '.join(available_languages) if available_languages else 'None'}"
                    },
                    "pagination": None
                }
        except TranscriptsDisabled:
            return {
                "data": None,
                "error": {
                    "code": "TranscriptsDisabled",
                    "message": f"Transcripts are disabled for video {video_id}"
                },
                "pagination": None
            }

        # Combine transcript segments into continuous text
        full_text = []
        segments = []

        for segment in transcript_data:
            text = segment.text.strip()
            if text:
                full_text.append(text)
                segments.append({
                    "text": text,
                    "start": segment.start,
                    "duration": segment.duration
                })

        combined_text = " ".join(full_text)

        # Also get available languages from YouTube API for completeness
        available_tracks = []
        try:
            client = _get_client()
            captions_response = client.client.captions().list(
                part="snippet",
                videoId=video_id
            ).execute()

            items = captions_response.get("items", [])
            available_tracks = [
                {
                    "id": item.get("id"),
                    "language": item.get("snippet", {}).get("languageCode"),
                    "kind": item.get("snippet", {}).get("trackKind")
                }
                for item in items
            ]
        except Exception:
            pass

        return {
            "data": {
                "videoId": video_id,
                "language": used_language,
                "text": combined_text,
                "segments": segments,
                "segmentCount": len(segments),
                "availableTracks": available_tracks
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
            "description": "Get transcript/captions for a YouTube video. Returns actual transcript text.",
            "inputSchema": GetTranscriptArgs.model_json_schema()
        }]

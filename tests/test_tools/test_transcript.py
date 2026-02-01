"""Unit tests for youtube_get_transcript tool."""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from src.tools.transcript import youtube_get_transcript, GetTranscriptArgs


@pytest.mark.unit
class TestGetTranscriptArgs:
    """Test GetTranscriptArgs Pydantic model."""

    def test_get_transcript_args_defaults(self):
        """GetTranscriptArgs should use defaults correctly."""
        args = GetTranscriptArgs(video_id="abc123")
        assert args.video_id == "abc123"
        assert args.language == "en"


@pytest.mark.unit
class TestYouTubeGetTranscript:
    """Test youtube_get_transcript function."""

    @pytest.mark.asyncio
    async def test_get_transcript_success(self):
        """youtube_get_transcript should return transcript data."""
        with patch("src.tools.transcript.YouTubeClient") as MockYouTubeClient:
            mock_client_instance = MockYouTubeClient.return_value.return_value = MagicMock()
            mock_transcript_api = MagicMock()

            mock_transcript_data = [
                Mock(text="Hello world", start=0.0, duration=1.0),
                Mock(text="This is a test", start=1.0, duration=1.0),
            ]
            mock_transcript_api.fetch.return_value = mock_transcript_data
            mock_transcript_api.list.return_value = []

        result = await youtube_get_transcript(video_id="abc123", language="en")

        assert result["data"]["videoId"] == "abc123"
        assert result["data"]["language"] == "en"
        assert result["data"]["segmentCount"] == 2
        assert result["error"] is None

    @pytest.mark.asyncio
    async def test_get_transcript_no_transcript_available(self):
        """youtube_get_transcript should return NotFound when no transcript available."""
        with patch("src.tools.transcript.YouTubeClient") as MockYouTubeClient:
            mock_client_instance = MockYouTubeClient.return_value.return_value = MagicMock()
            mock_transcript_api = MagicMock()
            mock_transcript_api.fetch.return_value = []
            mock_transcript_api.list.return_value = []

            from youtube_transcript_api import NoTranscriptFound
            mock_transcript_api.fetch.side_effect = NoTranscriptFound("No transcript found")

        result = await youtube_get_transcript(video_id="abc123")

        assert result["data"] is None
        assert result["error"]["code"] == "NotFound"

    @pytest.mark.asyncio
    async def test_get_transcript_transcripts_disabled(self):
        """youtube_get_transcript should return error when transcripts disabled."""
        with patch("src.tools.transcript.YouTubeClient") as MockYouTubeClient:
            mock_client_instance = MockYouTubeClient.return_value.return_value = MagicMock()
            mock_transcript_api = MagicMock()
            mock_transcript_api.fetch.return_value = []

            from youtube_transcript_api import TranscriptsDisabled
            mock_transcript_api.fetch.side_effect = TranscriptsDisabled("Transcripts disabled")

        result = await youtube_get_transcript(video_id="abc123")

        assert result["data"] is None
        assert result["error"]["code"] == "TranscriptsDisabled"
        assert "disabled" in result["error"]["message"]

    @pytest.mark.asyncio
    async def test_get_transcript_handles_exception(self):
        """youtube_get_transcript should handle API exceptions gracefully."""
        with patch("src.tools.transcript.YouTubeClient") as MockYouTubeClient:
            mock_client_instance = MockYouTubeClient.return_value.return_value = MagicMock()
            mock_transcript_api = MagicMock()
            mock_transcript_api.fetch.side_effect = Exception("API Error")

        result = await youtube_get_transcript(video_id="abc123")

        assert result["data"] is None
        assert result["error"]["code"] == "Exception"
        assert result["pagination"] is None

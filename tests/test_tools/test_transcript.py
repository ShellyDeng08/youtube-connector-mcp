"""Unit tests for youtube_get_transcript tool."""
import pytest
import os
from unittest.mock import Mock, patch
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
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.transcript._client", None)
    @patch("src.tools.transcript.YouTubeClient")
    async def test_get_transcript_finds_requested_language(self, mock_client_class):
        """youtube_get_transcript should find caption in requested language."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_captions = Mock()
        mock_captions.list.return_value.execute.return_value = {
            "items": [
                {"id": "en_cap", "snippet": {"languageCode": "en", "trackKind": "standard"}},
                {"id": "es_cap", "snippet": {"languageCode": "es", "trackKind": "standard"}}
            ]
        }
        mock_client_instance.client.captions.return_value = mock_captions

        result = await youtube_get_transcript(video_id="abc123", language="en")

        assert result["data"]["language"] == "en"
        assert result["data"]["captionId"] == "en_cap"
        assert len(result["data"]["availableTracks"]) == 2
        assert result["error"] is None

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.transcript._client", None)
    @patch("src.tools.transcript.YouTubeClient")
    async def test_get_transcript_falls_back_to_asr(self, mock_client_class):
        """youtube_get_transcript should fall back to auto-generated (asr) if no exact match."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_captions = Mock()
        mock_captions.list.return_value.execute.return_value = {
            "items": [
                {"id": "asr_cap", "snippet": {"languageCode": "en", "trackKind": "asr"}},
                {"id": "es_cap", "snippet": {"languageCode": "es", "trackKind": "standard"}}
            ]
        }
        mock_client_instance.client.captions.return_value = mock_captions

        result = await youtube_get_transcript(video_id="abc123", language="en")

        assert result["data"]["captionId"] == "asr_cap"
        assert result["error"] is None

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.transcript._client", None)
    @patch("src.tools.transcript.YouTubeClient")
    async def test_get_transcript_falls_back_to_first_available(self, mock_client_class):
        """youtube_get_transcript should fall back to first available if no ASR."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_captions = Mock()
        mock_captions.list.return_value.execute.return_value = {
            "items": [
                {"id": "es_cap", "snippet": {"languageCode": "es", "trackKind": "standard"}}
            ]
        }
        mock_client_instance.client.captions.return_value = mock_captions

        result = await youtube_get_transcript(video_id="abc123", language="en")

        assert result["data"]["captionId"] == "es_cap"
        assert result["error"] is None

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.transcript._client", None)
    @patch("src.tools.transcript.YouTubeClient")
    async def test_get_transcript_no_captions_returns_error(self, mock_client_class):
        """youtube_get_transcript should return NotFound when no captions available."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_captions = Mock()
        mock_captions.list.return_value.execute.return_value = {"items": []}
        mock_client_instance.client.captions.return_value = mock_captions

        result = await youtube_get_transcript(video_id="abc123")

        assert result["data"] is None
        assert result["error"]["code"] == "NotFound"
        assert "captions" in result["error"]["message"].lower()
        assert "abc123" in result["error"]["message"]
        assert result["error"]["message"] == "No captions available for video abc123 in language en"

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.transcript._client", None)
    @patch("src.tools.transcript.YouTubeClient")
    async def test_get_transcript_handles_api_exception(self, mock_client_class):
        """youtube_get_transcript should handle API exceptions gracefully."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_captions = Mock()
        mock_captions.list.return_value.execute.side_effect = Exception("API Error")
        mock_client_instance.client.captions.return_value = mock_captions

        result = await youtube_get_transcript(video_id="abc123")

        assert result["data"] is None
        assert result["error"]["code"] == "Exception"
        assert result["pagination"] is None

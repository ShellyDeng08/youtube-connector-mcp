"""Unit tests for youtube_get_video tool."""
import pytest
import os
from unittest.mock import Mock, patch
from src.tools.video import youtube_get_video, GetVideoArgs


@pytest.mark.unit
class TestGetVideoArgs:
    """Test GetVideoArgs Pydantic model."""

    def test_get_video_args_with_defaults(self):
        """GetVideoArgs should use defaults correctly."""
        args = GetVideoArgs(video_id="abc123")
        assert args.video_id == "abc123"
        assert args.part == ["snippet", "statistics", "contentDetails"]

    def test_get_video_args_custom_parts(self):
        """GetVideoArgs should accept custom parts."""
        args = GetVideoArgs(video_id="abc123", part=["snippet", "contentDetails"])
        assert args.video_id == "abc123"
        assert args.part == ["snippet", "contentDetails"]


@pytest.mark.unit
class TestYouTubeGetVideo:
    """Test youtube_get_video function."""

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.video._client", None)
    @patch("src.tools.video.YouTubeClient")
    async def test_get_video_success(self, mock_client_class):
        """youtube_get_video should return video details on success."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_videos = Mock()
        mock_videos.list.return_value.execute.return_value = {
            "items": [{
                "id": "abc123",
                "snippet": {"title": "Test Video"},
                "statistics": {"viewCount": "1000"}
            }]
        }
        mock_client_instance.client.videos.return_value = mock_videos

        result = await youtube_get_video(video_id="abc123")

        assert result["data"]["id"] == "abc123"
        assert result["error"] is None
        assert result["pagination"] is None

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.video._client", None)
    @patch("src.tools.video.YouTubeClient")
    async def test_get_video_not_found(self, mock_client_class):
        """youtube_get_video should return NotFound error for missing video."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_videos = Mock()
        mock_videos.list.return_value.execute.return_value = {"items": []}
        mock_client_instance.client.videos.return_value = mock_videos

        result = await youtube_get_video(video_id="nonexistent")

        assert result["data"] is None
        assert result["error"]["code"] == "NotFound"
        assert "nonexistent" in result["error"]["message"]
        assert result["pagination"] is None

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.video._client", None)
    @patch("src.tools.video.YouTubeClient")
    async def test_get_video_custom_part(self, mock_client_class):
        """youtube_get_video should use custom part parameter."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_videos = Mock()
        mock_videos.list.return_value.execute.return_value = {"items": [{"id": "abc123"}]}
        mock_client_instance.client.videos.return_value = mock_videos

        await youtube_get_video(video_id="abc123", part=["snippet"])

        call_args = mock_videos.list.call_args
        assert call_args[1]["part"] == "snippet"

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.video._client", None)
    @patch("src.tools.video.YouTubeClient")
    async def test_get_video_handles_api_exception(self, mock_client_class):
        """youtube_get_video should handle API exceptions gracefully."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_videos = Mock()
        mock_videos.list.return_value.execute.side_effect = Exception("API Error")
        mock_client_instance.client.videos.return_value = mock_videos

        result = await youtube_get_video(video_id="abc123")

        assert result["data"] is None
        assert result["error"]["code"] == "Exception"
        assert result["pagination"] is None

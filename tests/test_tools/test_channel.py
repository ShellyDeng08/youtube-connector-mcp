"""Unit tests for youtube_get_channel tool."""
import pytest
import os
from unittest.mock import Mock, patch
from src.tools.channel import youtube_get_channel, GetChannelArgs


@pytest.mark.unit
class TestGetChannelArgs:
    """Test GetChannelArgs Pydantic model."""

    def test_get_channel_args_defaults(self):
        """GetChannelArgs should have optional fields."""
        args = GetChannelArgs(channel_id="UCabc123")
        assert args.channel_id == "UCabc123"
        assert args.username is None

    def test_get_channel_args_username(self):
        """GetChannelArgs should accept username."""
        args = GetChannelArgs(username="testchannel")
        assert args.channel_id is None
        assert args.username == "testchannel"


@pytest.mark.unit
class TestYouTubeGetChannel:
    """Test youtube_get_channel function."""

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.channel._client", None)
    @patch("src.tools.channel.YouTubeClient")
    async def test_get_channel_by_id_success(self, mock_client_class):
        """youtube_get_channel should work with channel ID."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_channels = Mock()
        mock_channels.list.return_value.execute.return_value = {
            "items": [{
                "id": "UCabc123",
                "snippet": {"title": "Test Channel"},
                "statistics": {"subscriberCount": "10000"}
            }]
        }
        mock_client_instance.client.channels.return_value = mock_channels

        result = await youtube_get_channel(channel_id="UCabc123")

        assert result["data"]["id"] == "UCabc123"
        assert result["error"] is None

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.channel._client", None)
    @patch("src.tools.channel.YouTubeClient")
    async def test_get_channel_by_username_strips_at(self, mock_client_class):
        """youtube_get_channel should strip @ from username."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_channels = Mock()
        mock_channels.list.return_value.execute.return_value = {
            "items": [{"id": "UCabc123", "snippet": {"title": "Test"}}]
        }
        mock_client_instance.client.channels.return_value = mock_channels

        await youtube_get_channel(username="@testchannel")

        call_args = mock_channels.list.call_args
        assert call_args[1]["forUsername"] == "testchannel"

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.channel._client", None)
    @patch("src.tools.channel.YouTubeClient")
    async def test_get_channel_no_id_or_username(self, mock_client_class):
        """youtube_get_channel should return InvalidInput when no ID or username."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        result = await youtube_get_channel()

        assert result["data"] is None
        assert result["error"]["code"] == "InvalidInput"
        assert "required" in result["error"]["message"].lower()

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.channel._client", None)
    @patch("src.tools.channel.YouTubeClient")
    async def test_get_channel_not_found(self, mock_client_class):
        """youtube_get_channel should return NotFound for missing channel."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_channels = Mock()
        mock_channels.list.return_value.execute.return_value = {"items": []}
        mock_client_instance.client.channels.return_value = mock_channels

        result = await youtube_get_channel(channel_id="nonexistent")

        assert result["data"] is None
        assert result["error"]["code"] == "NotFound"

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.channel._client", None)
    @patch("src.tools.channel.YouTubeClient")
    async def test_get_channel_handles_api_exception(self, mock_client_class):
        """youtube_get_channel should handle API exceptions gracefully."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_channels = Mock()
        mock_channels.list.return_value.execute.side_effect = Exception("API Error")
        mock_client_instance.client.channels.return_value = mock_channels

        result = await youtube_get_channel(channel_id="UCabc123")

        assert result["data"] is None
        assert result["error"]["code"] == "Exception"

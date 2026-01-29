"""Unit tests for youtube_get_playlist and youtube_list_playlists tools."""
import pytest
import os
from unittest.mock import Mock, patch
from src.tools.playlist import youtube_get_playlist, youtube_list_playlists, GetPlaylistArgs, ListPlaylistsArgs


@pytest.mark.unit
class TestGetPlaylistArgs:
    """Test GetPlaylistArgs Pydantic model."""

    def test_get_playlist_args_defaults(self):
        """GetPlaylistArgs should use defaults correctly."""
        args = GetPlaylistArgs(playlist_id="PLabc123")
        assert args.playlist_id == "PLabc123"
        assert args.max_results == 50


@pytest.mark.unit
class TestListPlaylistsArgs:
    """Test ListPlaylistsArgs Pydantic model."""

    def test_list_playlists_args_defaults(self):
        """ListPlaylistsArgs should use defaults correctly."""
        args = ListPlaylistsArgs(channel_id="UCabc123")
        assert args.channel_id == "UCabc123"
        assert args.max_results == 25


@pytest.mark.unit
class TestYouTubeGetPlaylist:
    """Test youtube_get_playlist function."""

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.playlist._client", None)
    @patch("src.tools.playlist.YouTubeClient")
    async def test_get_playlist_success(self, mock_client_class):
        """youtube_get_playlist should return playlist data on success."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_items = Mock()
        mock_items.list.return_value.execute.return_value = {
            "items": [{"id": "item1"}],
            "nextPageToken": "next123",
            "pageInfo": {"totalResults": 10}
        }
        mock_client_instance.client.playlistItems.return_value = mock_items

        mock_playlists = Mock()
        mock_playlists.list.return_value.execute.return_value = {
            "items": [{"id": "PLabc123", "snippet": {"title": "Test Playlist"}}]
        }
        mock_client_instance.client.playlists.return_value = mock_playlists

        result = await youtube_get_playlist(playlist_id="PLabc123")

        assert result["data"]["details"]["id"] == "PLabc123"
        assert len(result["data"]["items"]) == 1
        assert result["error"] is None
        assert result["pagination"]["nextPageToken"] == "next123"

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.playlist._client", None)
    @patch("src.tools.playlist.YouTubeClient")
    async def test_get_playlist_max_results_capped_at_50(self, mock_client_class):
        """youtube_get_playlist should cap max_results at 50."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_items = Mock()
        mock_items.list.return_value.execute.return_value = {"items": [], "pageInfo": {"totalResults": 0}}
        mock_client_instance.client.playlistItems.return_value = mock_items

        mock_playlists = Mock()
        mock_playlists.list.return_value.execute.return_value = {"items": [{"id": "PLabc123"}]}
        mock_client_instance.client.playlists.return_value = mock_playlists

        await youtube_get_playlist(playlist_id="PLabc123", max_results=100)

        call_args = mock_items.list.call_args
        assert call_args[1]["maxResults"] == 50

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.playlist._client", None)
    @patch("src.tools.playlist.YouTubeClient")
    async def test_get_playlist_handles_api_exception(self, mock_client_class):
        """youtube_get_playlist should handle API exceptions gracefully."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_items = Mock()
        mock_items.list.return_value.execute.side_effect = Exception("API Error")
        mock_client_instance.client.playlistItems.return_value = mock_items

        result = await youtube_get_playlist(playlist_id="PLabc123")

        assert result["data"] is None
        assert result["error"]["code"] == "Exception"
        assert result["pagination"] is None


@pytest.mark.unit
class TestYouTubeListPlaylists:
    """Test youtube_list_playlists function."""

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.playlist._client", None)
    @patch("src.tools.playlist.YouTubeClient")
    async def test_list_playlists_success(self, mock_client_class):
        """youtube_list_playlists should return playlists on success."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_playlists = Mock()
        mock_playlists.list.return_value.execute.return_value = {
            "items": [
                {"id": "PLabc123", "snippet": {"title": "Playlist 1"}},
                {"id": "PLdef456", "snippet": {"title": "Playlist 2"}}
            ],
            "nextPageToken": "next123",
            "pageInfo": {"totalResults": 20}
        }
        mock_client_instance.client.playlists.return_value = mock_playlists

        result = await youtube_list_playlists(channel_id="UCabc123")

        assert len(result["data"]) == 2
        assert result["error"] is None
        assert result["pagination"]["nextPageToken"] == "next123"
        assert result["pagination"]["totalResults"] == 20

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.playlist._client", None)
    @patch("src.tools.playlist.YouTubeClient")
    async def test_list_playlists_max_results_capped_at_50(self, mock_client_class):
        """youtube_list_playlists should cap max_results at 50."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_playlists = Mock()
        mock_playlists.list.return_value.execute.return_value = {"items": [], "pageInfo": {"totalResults": 0}}
        mock_client_instance.client.playlists.return_value = mock_playlists

        await youtube_list_playlists(channel_id="UCabc123", max_results=100)

        call_args = mock_playlists.list.call_args
        assert call_args[1]["maxResults"] == 50

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.playlist._client", None)
    @patch("src.tools.playlist.YouTubeClient")
    async def test_list_playlists_handles_api_exception(self, mock_client_class):
        """youtube_list_playlists should handle API exceptions gracefully."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_playlists = Mock()
        mock_playlists.list.return_value.execute.side_effect = Exception("API Error")
        mock_client_instance.client.playlists.return_value = mock_playlists

        result = await youtube_list_playlists(channel_id="UCabc123")

        assert result["data"] is None
        assert result["error"]["code"] == "Exception"
        assert result["pagination"] is None

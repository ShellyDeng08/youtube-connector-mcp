"""Integration tests using real YouTube API."""
import pytest
import os
from tests.conftest import skip_if_no_api_key


@pytest.mark.integration
@skip_if_no_api_key()
class TestYouTubeSearchIntegration:
    """Integration tests for youtube_search with real API."""

    @pytest.mark.asyncio
    async def test_search_real_videos(self, integration_api_key):
        """Search should return real videos from YouTube."""
        from src.tools.search import youtube_search

        # Set API key
        os.environ["YOUTUBE_API_KEY"] = integration_api_key

        # Reset client
        from src.tools import search
        search._client = None

        result = await youtube_search(query="Python programming tutorial", max_results=5)

        assert result["error"] is None
        assert result["data"]
        assert len(result["data"]) > 0
        assert len(result["data"]) <= 5

        # Verify structure
        first_item = result["data"][0]
        assert "id" in first_item
        assert "snippet" in first_item
        assert "title" in first_item["snippet"]

    @pytest.mark.asyncio
    async def test_search_preserves_pagination(self, integration_api_key):
        """Search should return pagination tokens."""
        from src.tools.search import youtube_search

        os.environ["YOUTUBE_API_KEY"] = integration_api_key
        from src.tools import search
        search._client = None

        result = await youtube_search(query="Python", max_results=50)

        # With popular search term, should get pagination
        if result["pagination"]["totalResults"] > 50:
            assert result["pagination"]["nextPageToken"]


@pytest.mark.integration
@skip_if_no_api_key()
class TestYouTubeGetVideoIntegration:
    """Integration tests for youtube_get_video with real API."""

    @pytest.mark.asyncio
    async def test_get_video_real_data(self, integration_api_key):
        """Get video should return real video data."""
        from src.tools.video import youtube_get_video

        os.environ["YOUTUBE_API_KEY"] = integration_api_key
        from src.tools import video
        video._client = None

        # Use a known video ID
        result = await youtube_get_video(video_id="dQw4w9WxXcQ")

        assert result["error"] is None
        assert result["data"]
        assert result["data"]["id"] == "dQw4w9WxXcQ"

        # Verify statistics exist
        assert "statistics" in result["data"]
        stats = result["data"]["statistics"]
        assert "viewCount" in stats
        assert int(stats["viewCount"]) > 0


@pytest.mark.integration
@skip_if_no_api_key()
class TestYouTubeGetChannelIntegration:
    """Integration tests for youtube_get_channel with real API."""

    @pytest.mark.asyncio
    async def test_get_channel_real_data(self, integration_api_key):
        """Get channel should return real channel data."""
        from src.tools.channel import youtube_get_channel

        os.environ["YOUTUBE_API_KEY"] = integration_api_key
        from src.tools import channel
        channel._client = None

        # Use Google Developers channel ID
        result = await youtube_get_channel(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw")

        assert result["error"] is None
        assert result["data"]
        assert result["data"]["id"] == "UC_x5XG1OV2P6uZZ5FSM9Ttw"

        # Verify statistics exist
        assert "statistics" in result["data"]
        stats = result["data"]["statistics"]
        assert "subscriberCount" in stats


@pytest.mark.integration
@skip_if_no_api_key()
class TestYouTubeGetCommentsIntegration:
    """Integration tests for youtube_get_comments with real API."""

    @pytest.mark.asyncio
    async def test_get_comments_real_data(self, integration_api_key):
        """Get comments should return real comment data."""
        from src.tools.comments import youtube_get_comments

        os.environ["YOUTUBE_API_KEY"] = integration_api_key
        from src.tools import comments
        comments._client = None

        # Use a known video ID
        result = await youtube_get_comments(video_id="dQw4w9WxXcQ", max_results=5)

        assert result["error"] is None
        assert result["data"]
        assert len(result["data"]) >= 0

        # Verify comment structure if any
        if result["data"]:
            first_comment = result["data"][0]
            assert "snippet" in first_comment
            assert "topLevelComment" in first_comment["snippet"]


@pytest.mark.integration
@skip_if_no_api_key()
class TestYouTubeGetPlaylistIntegration:
    """Integration tests for youtube_get_playlist with real API."""

    @pytest.mark.asyncio
    async def test_get_playlist_real_data(self, integration_api_key):
        """Get playlist should return real playlist data."""
        from src.tools.playlist import youtube_get_playlist

        os.environ["YOUTUBE_API_KEY"] = integration_api_key
        from src.tools import playlist
        playlist._client = None

        # Use a real playlist ID
        result = await youtube_get_playlist(playlist_id="PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf", max_results=5)

        assert result["error"] is None
        assert result["data"]
        assert "details" in result["data"]
        assert "items" in result["data"]


@pytest.mark.integration
@skip_if_no_api_key()
class TestYouTubeListPlaylistsIntegration:
    """Integration tests for youtube_list_playlists with real API."""

    @pytest.mark.asyncio
    async def test_list_playlists_real_data(self, integration_api_key):
        """List playlists should return real playlist data."""
        from src.tools.playlist import youtube_list_playlists

        os.environ["YOUTUBE_API_KEY"] = integration_api_key
        from src.tools import playlist
        playlist._client = None

        # Use Google Developers channel
        result = await youtube_list_playlists(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", max_results=5)

        assert result["error"] is None
        assert result["data"]
        assert len(result["data"]) >= 0


@pytest.mark.integration
@skip_if_no_api_key()
class TestYouTubeGetTranscriptIntegration:
    """Integration tests for youtube_get_transcript with real API."""

    @pytest.mark.asyncio
    async def test_get_transcript_real_data(self, integration_api_key):
        """Get transcript should return available caption tracks."""
        from src.tools.transcript import youtube_get_transcript

        os.environ["YOUTUBE_API_KEY"] = integration_api_key
        from src.tools import transcript
        transcript._client = None

        # Use a video that likely has captions
        result = await youtube_get_transcript(video_id="dQw4w9WxXcQ", language="en")

        # May or may not have captions
        if result["error"] is None:
            assert result["data"]
            assert "availableTracks" in result["data"]

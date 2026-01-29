"""Unit tests for youtube_get_comments tool."""
import pytest
import os
from unittest.mock import Mock, patch
from src.tools.comments import youtube_get_comments, GetCommentsArgs


@pytest.mark.unit
class TestGetCommentsArgs:
    """Test GetCommentsArgs Pydantic model."""

    def test_get_comments_args_defaults(self):
        """GetCommentsArgs should use defaults correctly."""
        args = GetCommentsArgs(video_id="abc123")
        assert args.video_id == "abc123"
        assert args.max_results == 20
        assert args.page_token is None


@pytest.mark.unit
class TestYouTubeGetComments:
    """Test youtube_get_comments function."""

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.comments._client", None)
    @patch("src.tools.comments.YouTubeClient")
    async def test_get_comments_success(self, mock_client_class):
        """youtube_get_comments should return comments on success."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_threads = Mock()
        mock_threads.list.return_value.execute.return_value = {
            "items": [
                {"id": "comment1", "snippet": {"topLevelComment": {"snippet": {"textDisplay": "Test 1"}}}},
                {"id": "comment2", "snippet": {"topLevelComment": {"snippet": {"textDisplay": "Test 2"}}}}
            ],
            "nextPageToken": "next123",
            "pageInfo": {"totalResults": 50}
        }
        mock_client_instance.client.commentThreads.return_value = mock_threads

        result = await youtube_get_comments(video_id="abc123")

        assert len(result["data"]) == 2
        assert result["error"] is None
        assert result["pagination"]["nextPageToken"] == "next123"
        assert result["pagination"]["totalResults"] == 50

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.comments._client", None)
    @patch("src.tools.comments.YouTubeClient")
    async def test_get_comments_max_results_capped_at_100(self, mock_client_class):
        """youtube_get_comments should cap max_results at 100."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_threads = Mock()
        mock_threads.list.return_value.execute.return_value = {"items": [], "pageInfo": {"totalResults": 0}}
        mock_client_instance.client.commentThreads.return_value = mock_threads

        await youtube_get_comments(video_id="abc123", max_results=200)

        call_args = mock_threads.list.call_args
        assert call_args[1]["maxResults"] == 100

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.comments._client", None)
    @patch("src.tools.comments.YouTubeClient")
    async def test_get_comments_with_page_token(self, mock_client_class):
        """youtube_get_comments should pass page_token to API."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_threads = Mock()
        mock_threads.list.return_value.execute.return_value = {"items": [], "pageInfo": {"totalResults": 0}}
        mock_client_instance.client.commentThreads.return_value = mock_threads

        await youtube_get_comments(video_id="abc123", page_token="token123")

        call_args = mock_threads.list.call_args
        assert call_args[1]["pageToken"] == "token123"

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.comments._client", None)
    @patch("src.tools.comments.YouTubeClient")
    async def test_get_comments_defaults_to_relevance_order(self, mock_client_class):
        """youtube_get_comments should default to relevance order."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_threads = Mock()
        mock_threads.list.return_value.execute.return_value = {"items": [], "pageInfo": {"totalResults": 0}}
        mock_client_instance.client.commentThreads.return_value = mock_threads

        await youtube_get_comments(video_id="abc123")

        call_args = mock_threads.list.call_args
        assert call_args[1]["order"] == "relevance"

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.comments._client", None)
    @patch("src.tools.comments.YouTubeClient")
    async def test_get_comments_handles_api_exception(self, mock_client_class):
        """youtube_get_comments should handle API exceptions gracefully."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_threads = Mock()
        mock_threads.list.return_value.execute.side_effect = Exception("API Error")
        mock_client_instance.client.commentThreads.return_value = mock_threads

        result = await youtube_get_comments(video_id="abc123")

        assert result["data"] is None
        assert result["error"]["code"] == "Exception"
        assert result["pagination"] is None

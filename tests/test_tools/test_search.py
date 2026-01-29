"""Unit tests for youtube_search tool."""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from src.tools.search import youtube_search, SearchArgs


@pytest.mark.unit
class TestSearchArgs:
    """Test SearchArgs Pydantic model."""

    def test_search_args_with_defaults(self):
        """SearchArgs should use defaults correctly."""
        args = SearchArgs(query="python tutorial")
        assert args.query == "python tutorial"
        assert args.max_results == 10
        assert args.order == "relevance"
        assert args.type == "video"

    def test_search_args_custom_values(self):
        """SearchArgs should accept custom values."""
        args = SearchArgs(
            query="test",
            max_results=25,
            order="date",
            type="channel"
        )
        assert args.query == "test"
        assert args.max_results == 25
        assert args.order == "date"
        assert args.type == "channel"

    def test_search_args_max_results_validation(self):
        """max_results should be in valid range."""
        # Valid values
        SearchArgs(query="test", max_results=1)
        SearchArgs(query="test", max_results=50)
        # Pydantic will validate on the field level if we add validators


@pytest.mark.unit
class TestYouTubeSearch:
    """Test youtube_search function."""

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.search._client", None)
    @patch("src.tools.search.YouTubeClient")
    async def test_search_success(self, mock_client_class):
        """youtube_search should return results on success."""
        # Setup mock client
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_search = Mock()
        mock_search.list.return_value.execute.return_value = {
            "items": [
                {
                    "id": {"kind": "youtube#video", "videoId": "video1"},
                    "snippet": {"title": "Test Video"}
                }
            ],
            "nextPageToken": "token123",
            "pageInfo": {"totalResults": 100}
        }
        mock_client_instance.client.search.return_value = mock_search

        # Call function
        result = await youtube_search(query="python tutorial", max_results=10)

        # Verify result structure
        assert result["data"]
        assert len(result["data"]) == 1
        assert result["data"][0]["snippet"]["title"] == "Test Video"
        assert result["error"] is None
        assert result["pagination"]["nextPageToken"] == "token123"
        assert result["pagination"]["totalResults"] == 100

        # Verify API was called correctly
        mock_search.list.assert_called_once()
        call_args = mock_search.list.call_args
        assert call_args[1]["q"] == "python tutorial"
        assert call_args[1]["maxResults"] == 10
        assert call_args[1]["order"] == "relevance"
        assert call_args[1]["type"] == "video"

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.search._client", None)
    @patch("src.tools.search.YouTubeClient")
    async def test_search_max_results_capped_at_50(self, mock_client_class):
        """youtube_search should cap max_results at 50."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_search = Mock()
        mock_search.list.return_value.execute.return_value = {"items": [], "pageInfo": {"totalResults": 0}}
        mock_client_instance.client.search.return_value = mock_search

        # Request 100, should cap at 50
        await youtube_search(query="test", max_results=100)

        call_args = mock_search.list.call_args
        assert call_args[1]["maxResults"] == 50

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.search._client", None)
    @patch("src.tools.search.YouTubeClient")
    async def test_search_order_parameter(self, mock_client_class):
        """youtube_search should pass order parameter to API."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_search = Mock()
        mock_search.list.return_value.execute.return_value = {"items": [], "pageInfo": {"totalResults": 0}}
        mock_client_instance.client.search.return_value = mock_search

        await youtube_search(query="test", order="viewCount")

        call_args = mock_search.list.call_args
        assert call_args[1]["order"] == "viewCount"

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.search._client", None)
    @patch("src.tools.search.YouTubeClient")
    async def test_search_type_parameter(self, mock_client_class):
        """youtube_search should pass type parameter to API."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_search = Mock()
        mock_search.list.return_value.execute.return_value = {"items": [], "pageInfo": {"totalResults": 0}}
        mock_client_instance.client.search.return_value = mock_search

        await youtube_search(query="test", type="channel")

        call_args = mock_search.list.call_args
        assert call_args[1]["type"] == "channel"

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.search._client", None)
    @patch("src.tools.search.YouTubeClient")
    async def test_search_handles_empty_results(self, mock_client_class):
        """youtube_search should handle empty results."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_search = Mock()
        mock_search.list.return_value.execute.return_value = {
            "items": [],
            "pageInfo": {"totalResults": 0}
        }
        mock_client_instance.client.search.return_value = mock_search

        result = await youtube_search(query="test")

        assert result["data"] == []
        assert result["error"] is None

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.search._client", None)
    @patch("src.tools.search.YouTubeClient")
    async def test_search_preserves_pagination_token(self, mock_client_class):
        """youtube_search should preserve nextPageToken."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_search = Mock()
        mock_search.list.return_value.execute.return_value = {
            "items": [{"id": "video1"}],
            "nextPageToken": "CAUQAA",
            "pageInfo": {"totalResults": 100}
        }
        mock_client_instance.client.search.return_value = mock_search

        result = await youtube_search(query="test")

        assert result["pagination"]["nextPageToken"] == "CAUQAA"

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.search._client", None)
    @patch("src.tools.search.YouTubeClient")
    async def test_search_handles_api_exception(self, mock_client_class):
        """youtube_search should handle API exceptions gracefully."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_search = Mock()
        mock_search.list.return_value.execute.side_effect = Exception("API Error")
        mock_client_instance.client.search.return_value = mock_search

        result = await youtube_search(query="test")

        assert result["data"] is None
        assert result["error"]["code"] == "Exception"
        assert result["error"]["message"] == "API Error"
        assert result["pagination"] is None

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.search._client", None)
    @patch("src.tools.search.YouTubeClient")
    async def test_search_handles_quota_exceeded(self, mock_client_class):
        """youtube_search should handle quota exceeded errors."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_search = Mock()
        mock_search.list.return_value.execute.side_effect = Exception("Quota exceeded")
        mock_client_instance.client.search.return_value = mock_search

        result = await youtube_search(query="test")

        assert result["data"] is None
        assert result["error"]["code"] == "Exception"
        assert "quota" in result["error"]["message"].lower()

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"YOUTUBE_API_KEY": "test_key"})
    @patch("src.tools.search._client", None)
    @patch("src.tools.search.YouTubeClient")
    async def test_search_uses_correct_parts(self, mock_client_class):
        """youtube_search should request correct API parts."""
        mock_client_instance = Mock()
        mock_client_class.return_value = mock_client_instance

        mock_search = Mock()
        mock_search.list.return_value.execute.return_value = {"items": [], "pageInfo": {"totalResults": 0}}
        mock_client_instance.client.search.return_value = mock_search

        await youtube_search(query="test")

        call_args = mock_search.list.call_args
        assert "part" in call_args[1]
        assert call_args[1]["part"] == "id,snippet"

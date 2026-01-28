"""Test fixtures."""
import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_youtube_client():
    """Mock YouTube client for testing."""
    client = Mock()
    client.search.return_value = MagicMock()
    client.videos.return_value = MagicMock()
    client.channels.return_value = MagicMock()
    client.commentThreads.return_value = MagicMock()
    client.captions.return_value = MagicMock()
    client.playlists.return_value = MagicMock()
    return client


@pytest.fixture
def sample_video_response():
    """Sample video API response."""
    return {
        "items": [{
            "id": "abc123",
            "snippet": {
                "title": "Test Video",
                "description": "Test description",
                "channelTitle": "Test Channel",
                "publishedAt": "2024-01-01T00:00:00Z",
                "thumbnails": {
                    "default": {"url": "https://example.com/thumb.jpg"}
                }
            },
            "statistics": {
                "viewCount": "1000",
                "likeCount": "100",
                "commentCount": "10"
            }
        }]
    }

"""Test fixtures."""
import pytest
import os
from unittest.mock import Mock, MagicMock


# Pytest markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers",
        "unit: marks tests as unit tests (with mocks, no API key)"
    )
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests (requires YOUTUBE_API_KEY_TEST)"
    )
    config.addinivalue_line(
        "markers",
        "mcp: marks tests as MCP protocol tests"
    )


# Test data IDs (real, public content for integration tests)
@pytest.fixture
def test_video_id():
    """A real, public video ID for integration tests."""
    return "dQw4w9WxXcQ"  # Rick Astley - Never Gonna Give You Up


@pytest.fixture
def test_channel_id():
    """A real channel ID for integration tests."""
    return "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Google Developers


@pytest.fixture
def test_playlist_id():
    """A real playlist ID for integration tests."""
    return "PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"  # Google Developers Python


# Integration test helpers
@pytest.fixture
def integration_api_key():
    """Get API key for integration tests. Returns None if not set."""
    return os.getenv("YOUTUBE_API_KEY_TEST")


def skip_if_no_api_key():
    """Skip test if no API key is available."""
    return pytest.mark.skipif(
        not os.getenv("YOUTUBE_API_KEY_TEST"),
        reason="YOUTUBE_API_KEY_TEST not set. Set it to run integration tests."
    )


# Mock fixtures
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
    client.playlistItems.return_value = MagicMock()
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
            },
            "contentDetails": {
                "duration": "PT10M30S",
                "definition": "hd"
            }
        }],
        "pageInfo": {
            "totalResults": 1,
            "resultsPerPage": 1
        }
    }


@pytest.fixture
def sample_search_response():
    """Sample search API response."""
    return {
        "items": [
            {
                "id": {"kind": "youtube#video", "videoId": "abc123"},
                "snippet": {
                    "title": "Test Video 1",
                    "description": "Test description 1",
                    "channelTitle": "Test Channel",
                    "publishedAt": "2024-01-01T00:00:00Z",
                    "thumbnails": {
                        "default": {"url": "https://example.com/thumb1.jpg"}
                    }
                }
            },
            {
                "id": {"kind": "youtube#video", "videoId": "def456"},
                "snippet": {
                    "title": "Test Video 2",
                    "description": "Test description 2",
                    "channelTitle": "Test Channel 2",
                    "publishedAt": "2024-01-02T00:00:00Z",
                    "thumbnails": {
                        "default": {"url": "https://example.com/thumb2.jpg"}
                    }
                }
            }
        ],
        "nextPageToken": "CAUQAA",
        "pageInfo": {
            "totalResults": 100,
            "resultsPerPage": 2
        }
    }


@pytest.fixture
def sample_channel_response():
    """Sample channel API response."""
    return {
        "items": [{
            "id": "UCabc123",
            "snippet": {
                "title": "Test Channel",
                "description": "Test channel description",
                "customUrl": "testchannel",
                "publishedAt": "2023-01-01T00:00:00Z",
                "thumbnails": {
                    "default": {"url": "https://example.com/channel.jpg"}
                }
            },
            "statistics": {
                "subscriberCount": "10000",
                "videoCount": "500",
                "viewCount": "1000000"
            },
            "contentDetails": {
                "relatedPlaylists": {
                    "uploads": "UUabc123",
                    "favorites": "FLabc123"
                }
            }
        }],
        "pageInfo": {
            "totalResults": 1,
            "resultsPerPage": 1
        }
    }


@pytest.fixture
def sample_comments_response():
    """Sample comments API response."""
    return {
        "items": [
            {
                "id": "comment1",
                "snippet": {
                    "topLevelComment": {
                        "id": "topcomment1",
                        "snippet": {
                            "authorDisplayName": "Test User 1",
                            "textDisplay": "Great video!",
                            "publishedAt": "2024-01-01T00:00:00Z",
                            "likeCount": "5"
                        }
                    },
                    "totalReplyCount": 2
                }
            },
            {
                "id": "comment2",
                "snippet": {
                    "topLevelComment": {
                        "id": "topcomment2",
                        "snippet": {
                            "authorDisplayName": "Test User 2",
                            "textDisplay": "Thanks for sharing",
                            "publishedAt": "2024-01-01T01:00:00Z",
                            "likeCount": "3"
                        }
                    },
                    "totalReplyCount": 0
                }
            }
        ],
        "nextPageToken": "nextPageToken123",
        "pageInfo": {
            "totalResults": 50,
            "resultsPerPage": 2
        }
    }


@pytest.fixture
def sample_playlist_response():
    """Sample playlist API response."""
    return {
        "items": [{
            "id": "PLplaylist123",
            "snippet": {
                "title": "Test Playlist",
                "description": "Test playlist description",
                "channelTitle": "Test Channel",
                "publishedAt": "2024-01-01T00:00:00Z"
            },
            "contentDetails": {
                "itemCount": "10"
            }
        }],
        "pageInfo": {
            "totalResults": 1,
            "resultsPerPage": 1
        }
    }


@pytest.fixture
def sample_playlist_items_response():
    """Sample playlist items API response."""
    return {
        "items": [
            {
                "id": "item1",
                "snippet": {
                    "title": "Video in Playlist 1",
                    "description": "Description 1",
                    "videoId": "video1",
                    "position": 1,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": "video1"
                    }
                }
            },
            {
                "id": "item2",
                "snippet": {
                    "title": "Video in Playlist 2",
                    "description": "Description 2",
                    "videoId": "video2",
                    "position": 2,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": "video2"
                    }
                }
            }
        ],
        "nextPageToken": "playlistNextToken",
        "pageInfo": {
            "totalResults": 10,
            "resultsPerPage": 2
        }
    }


@pytest.fixture
def sample_captions_response():
    """Sample captions API response."""
    return {
        "items": [
            {
                "id": "en_caption",
                "snippet": {
                    "videoId": "video123",
                    "lastUpdated": "2024-01-01T00:00:00Z",
                    "language": "en",
                    "languageCode": "en",
                    "name": "English",
                    "audioTrackType": "primary",
                    "isCC": False,
                    "isAutoSynced": False,
                    "trackKind": "standard"
                }
            },
            {
                "id": "asr_caption",
                "snippet": {
                    "videoId": "video123",
                    "lastUpdated": "2024-01-01T00:00:00Z",
                    "language": "en",
                    "languageCode": "en",
                    "name": "English (auto-generated)",
                    "audioTrackType": "primary",
                    "isCC": False,
                    "isAutoSynced": True,
                    "trackKind": "asr"
                }
            },
            {
                "id": "es_caption",
                "snippet": {
                    "videoId": "video123",
                    "lastUpdated": "2024-01-01T00:00:00Z",
                    "language": "es",
                    "languageCode": "es",
                    "name": "Spanish",
                    "audioTrackType": "primary",
                    "isCC": False,
                    "isAutoSynced": False,
                    "trackKind": "standard"
                }
            }
        ]
    }


@pytest.fixture
def empty_response():
    """Empty API response (not found)."""
    return {
        "items": [],
        "pageInfo": {
            "totalResults": 0,
            "resultsPerPage": 0
        }
    }

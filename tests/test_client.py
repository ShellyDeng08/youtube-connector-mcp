"""Tests for YouTube client."""
from src.youtube_client import YouTubeClient


def test_client_initialization():
    client = YouTubeClient(api_key="test_key")
    assert client.api_key == "test_key"

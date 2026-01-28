"""Tests for YouTube channel tool."""
from src.tools.channel import youtube_get_channel


def test_youtube_get_channel_exists():
    assert callable(youtube_get_channel)

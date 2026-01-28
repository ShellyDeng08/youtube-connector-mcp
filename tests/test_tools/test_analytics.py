"""Tests for YouTube analytics tool."""
from src.tools.analytics import youtube_get_analytics


def test_youtube_get_analytics_exists():
    assert callable(youtube_get_analytics)

"""Tests for YouTube comments tool."""
from src.tools.comments import youtube_get_comments


def test_youtube_get_comments_exists():
    assert callable(youtube_get_comments)

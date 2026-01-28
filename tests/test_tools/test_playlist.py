"""Tests for YouTube playlist tools."""
from src.tools.playlist import youtube_get_playlist, youtube_list_playlists


def test_playlist_tools_exist():
    assert callable(youtube_get_playlist)
    assert callable(youtube_list_playlists)

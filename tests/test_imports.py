"""Test that all MCP server modules can be imported."""
import pytest


def test_import_main():
    """Test that main module can be imported."""
    from src.main import server, list_tools
    assert server is not None
    assert callable(list_tools)


def test_import_tools():
    """Test that each tool module can be imported."""
    from src.tools.search import youtube_search, SearchArgs
    from src.tools.video import youtube_get_video, GetVideoArgs
    from src.tools.transcript import youtube_get_transcript, GetTranscriptArgs
    from src.tools.playlist import youtube_get_playlist, youtube_list_playlists, GetPlaylistArgs, ListPlaylistsArgs
    from src.tools.comments import youtube_get_comments, GetCommentsArgs
    from src.tools.channel import youtube_get_channel, GetChannelArgs

    # Test actual function imports (not just modules)
    assert youtube_search is not None
    assert youtube_get_video is not None
    assert youtube_get_transcript is not None
    assert youtube_get_playlist is not None
    assert youtube_list_playlists is not None
    assert youtube_get_comments is not None
    assert youtube_get_channel is not None

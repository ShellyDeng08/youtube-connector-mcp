import pytest
from responses import Response
from src.tools.search import youtube_search

def test_youtube_search_basic():
    # This will be tested via MCP protocol
    # For now, test that function exists
    assert callable(youtube_search)

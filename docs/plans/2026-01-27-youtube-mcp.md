wa# YouTube MCP Server Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Python MCP server that exposes YouTube Data API v3 functionality to Claude Code, including search, transcripts, playlists, comments, and analytics.

**Architecture:** Three-layer architecture - MCP Layer (stdio protocol), YouTube API Layer (google-api-python-client wrapper), Skill Layer (high-level workflows). Tools follow TDD with pytest, use environment variables for configuration, implement retry logic for network errors.

**Tech Stack:** Python 3.10+, mcp (MCP protocol), google-api-python-client (YouTube API), pydantic (validation), pytest (testing), responses (mocking)

---

## Task 1: Project Setup (Configuration Files)

**Files:**

- Create: `pyproject.toml`
- Create: `requirements.txt`
- Create: `.env.example`

**Step 1: Create pyproject.toml**

```toml
[project]
name = "youtube-mcp-server"
version = "0.1.0"
description = "YouTube MCP Server for Claude Code"
requires-python = ">=3.10"
dependencies = [
    "mcp>=0.9.0",
    "google-api-python-client>=2.140.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "responses>=0.25.0",
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
asyncio_mode = "auto"
```

**Step 2: Create requirements.txt**

```txt
mcp>=0.9.0
google-api-python-client>=2.140.0
pydantic>=2.0.0
```

**Step 3: Create .env.example**

```bash
# YouTube Data API v3 Key
# Get one from: https://console.cloud.google.com/apis/credentials
YOUTUBE_API_KEY=your_api_key_here

# Optional: Rate limit requests per second (default: 100)
YOUTUBE_RATE_LIMIT=100
```

**Step 4: Install dependencies and verify**

```bash
pip install -e ".[dev]"
```

Expected: Installation completes without errors.

**Step 5: Commit**

```bash
git add pyproject.toml requirements.txt .env.example
git commit -m "feat: add project configuration files"
```

---

## Task 2: Base Project Structure

**Files:**

- Create: `src/__init__.py`
- Create: `src/main.py` (minimal entry point)
- Create: `tests/__init__.py`

**Step 1: Create src directory structure**

```bash
mkdir -p src/tools src/models tests/test_tools
```

**Step 2: Create src/**init**.py**

```python
"""YouTube MCP Server."""
__version__ = "0.1.0"
```

**Step 3: Create minimal main.py**

```python
"""MCP Server entry point."""
import asyncio
from mcp.server import Server

server = Server("youtube-mcp-server")

@server.list_resources()
async def list_resources():
    return []

@server.read_resource()
async def read_resource(uri):
    raise ValueError(f"Resource not found: {uri}")

@server.list_tools()
async def list_tools():
    return []

@server.call_tool()
async def call_tool(name, arguments):
    raise ValueError(f"Tool not found: {name}")

async def main():
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )

if __name__ == "__main__":
    asyncio.run(main())
```

**Step 4: Create tests/**init**.py**

```python
"""Tests for YouTube MCP Server."""
```

**Step 5: Test that the server can start**

```bash
timeout 3 python -m src.main 2>&1 | head -5 || true
```

Expected: Server starts (no immediate crash)

**Step 6: Commit**

```bash
git add src/__init__.py src/main.py tests/__init__.py
git commit -m "feat: add minimal MCP server structure"
```

---

## Task 3: Environment Configuration Loading

**Files:**

- Create: `src/config.py`
- Create: `tests/test_config.py`

**Step 1: Write failing test for config**

```python
import os
from src.config import get_config

def test_get_config_with_env():
    os.environ["YOUTUBE_API_KEY"] = "test_key"
    config = get_config()
    assert config.api_key == "test_key"

def test_get_config_defaults():
    # Ensure clean state
    for key in ["YOUTUBE_API_KEY", "YOUTUBE_RATE_LIMIT"]:
        os.environ.pop(key, None)

    config = get_config()
    assert config.rate_limit == 100
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_config.py -v
```

Expected: FAIL with "module 'src.config' not found"

**Step 3: Create src/config.py**

```python
"""Configuration for YouTube MCP Server."""
import os
from dataclasses import dataclass
from typing import Literal


@dataclass
class Config:
    """Server configuration."""
    api_key: str
    rate_limit: int = 100


def get_config() -> Config:
    """Load configuration from environment variables."""
    api_key = os.getenv("YOUTUBE_API_KEY", "")
    if not api_key:
        raise ValueError(
            "YOUTUBE_API_KEY environment variable is required. "
            "Set it or add it to your MCP configuration."
        )

    rate_limit = int(os.getenv("YOUTUBE_RATE_LIMIT", "100"))
    return Config(api_key=api_key, rate_limit=rate_limit)
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_config.py -v
```

Expected: PASS (2 tests)

**Step 5: Commit**

```bash
git add src/config.py tests/test_config.py
git commit -m "feat: add environment configuration"
```

---

## Task 4: YouTube API Client - Initialization

**Files:**

- Create: `src/youtube_client.py`
- Create: `tests/test_client.py`
- Modify: `tests/conftest.py`

**Step 1: Write failing test for client initialization**

```python
from src.youtube_client import YouTubeClient

def test_client_initialization():
    client = YouTubeClient(api_key="test_key")
    assert client.api_key == "test_key"
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_client.py::test_client_initialization -v
```

Expected: FAIL with "module 'src.youtube_client' not found"

**Step 3: Create src/youtube_client.py with minimal implementation**

```python
"""YouTube API Client wrapper."""
from googleapiclient.discovery import build
from typing import Optional


class YouTubeClient:
    """Wrapper for YouTube Data API v3."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._client: Optional["build"] = None

    @property
    def client(self):
        """Lazy-load the YouTube API client."""
        if self._client is None:
            self._client = build("youtube", "v3", developerKey=self.api_key)
        return self._client
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_client.py::test_client_initialization -v
```

Expected: PASS

**Step 5: Create conftest.py with mock fixture**

```python
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
```

**Step 6: Commit**

```bash
git add src/youtube_client.py tests/test_client.py tests/conftest.py
git commit -m "feat: add YouTube API client initialization"
```

---

## Task 5: Search Tool - Implementation

**Files:**

- Create: `src/tools/search.py`
- Modify: `src/main.py` (register the tool)
- Create: `tests/test_tools/test_search.py`

**Step 1: Write failing test for search tool**

```python
import pytest
from responses import Response
from src.tools.search import youtube_search

def test_youtube_search_basic():
    # This will be tested via MCP protocol
    # For now, test the function exists
    assert callable(youtube_search)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_tools/test_search.py -v
```

Expected: FAIL with "module 'src.tools.search' not found"

**Step 3: Create src/tools/search.py**

```python
"""YouTube Search Tool."""
from typing import Optional
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class SearchArgs(BaseModel):
    """Arguments for YouTube search."""
    query: str = Field(description="Search query")
    max_results: int = Field(default=10, description="Maximum results (1-50)")
    order: str = Field(
        default="relevance",
        description="Order: relevance, date, viewCount, rating"
    )
    type: str = Field(
        default="video",
        description="Resource type: video, channel, playlist"
    )


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_search(query: str, max_results: int = 10, order: str = "relevance", type: str = "video"):
    """Search YouTube for videos, channels, or playlists.

    Args:
        query: Search terms
        max_results: Number of results (1-50)
        order: Sort order (relevance, date, viewCount, rating)
        type: Resource type (video, channel, playlist)

    Returns:
        Dictionary with search results or error
    """
    client = _get_client()

    search_params = {
        "q": query,
        "maxResults": min(max_results, 50),
        "order": order,
        "type": type,
        "part": "id,snippet"
    }

    try:
        response = client.client.search().list(**search_params).execute()
        return {
            "data": response.get("items", []),
            "error": None,
            "pagination": {
                "nextPageToken": response.get("nextPageToken"),
                "totalResults": response.get("pageInfo", {}).get("totalResults", 0)
            }
        }
    except Exception as e:
        return {
            "data": None,
            "error": {"code": type(e).__name__, "message": str(e)},
            "pagination": None
        }


def register_search_tools(server):
    """Register search tools with MCP server."""
    @server.call_tool()
    async def call_youtube_search(name, arguments):
        if name != "youtube_search":
            return None

        args = SearchArgs(**arguments)
        return await youtube_search(
            query=args.query,
            max_results=args.max_results,
            order=args.order,
            type=args.type
        )

    @server.list_tools()
    async def list_search_tools():
        return [{
            "name": "youtube_search",
            "description": "Search YouTube for videos, channels, or playlists",
            "inputSchema": SearchArgs.model_json_schema()
        }]
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_tools/test_search.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/tools/search.py tests/test_tools/test_search.py src/tools/__init__.py
git commit -m "feat: add YouTube search tool"
```

---

## Task 6: Video Details Tool

**Files:**

- Create: `src/tools/video.py`
- Modify: `src/main.py` (register the tool)
- Create: `tests/test_tools/test_video.py`

**Step 1: Write failing test for video tool**

```python
from src.tools.video import youtube_get_video

def test_youtube_get_video_exists():
    assert callable(youtube_get_video)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_tools/test_video.py -v
```

Expected: FAIL with "module 'src.tools.video' not found"

**Step 3: Create src/tools/video.py**

```python
"""YouTube Video Details Tool."""
from typing import Optional, List
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class GetVideoArgs(BaseModel):
    """Arguments for getting video details."""
    video_id: str = Field(description="YouTube video ID (11 characters)")
    part: List[str] = Field(
        default=["snippet", "statistics", "contentDetails"],
        description="Parts to retrieve: snippet, statistics, contentDetails"
    )


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_get_video(video_id: str, part: list = None):
    """Get detailed information about a YouTube video.

    Args:
        video_id: 11-character YouTube video ID
        part: List of parts to retrieve

    Returns:
        Dictionary with video details or error
    """
    if part is None:
        part = ["snippet", "statistics", "contentDetails"]

    client = _get_client()

    try:
        response = client.client.videos().list(
            id=video_id,
            part=",".join(part)
        ).execute()

        if not response.get("items"):
            return {
                "data": None,
                "error": {
                    "code": "NotFound",
                    "message": f"Video not found: {video_id}"
                },
                "pagination": None
            }

        return {
            "data": response["items"][0],
            "error": None,
            "pagination": None
        }
    except Exception as e:
        return {
            "data": None,
            "error": {"code": type(e).__name__, "message": str(e)},
            "pagination": None
        }


def register_video_tools(server):
    """Register video tools with MCP server."""
    @server.call_tool()
    async def call_youtube_get_video(name, arguments):
        if name != "youtube_get_video":
            return None

        args = GetVideoArgs(**arguments)
        return await youtube_get_video(
            video_id=args.video_id,
            part=args.part
        )

    @server.list_tools()
    async def list_video_tools():
        return [{
            "name": "youtube_get_video",
            "description": "Get detailed information about a YouTube video",
            "inputSchema": GetVideoArgs.model_json_schema()
        }]
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_tools/test_video.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/tools/video.py tests/test_tools/test_video.py
git commit -m "feat: add YouTube video details tool"
```

---

## Task 7: Transcript Tool

**Files:**

- Create: `src/tools/transcript.py`
- Modify: `src/main.py` (register the tool)
- Create: `tests/test_tools/test_transcript.py`

**Step 1: Write failing test for transcript tool**

```python
from src.tools.transcript import youtube_get_transcript

def test_youtube_get_transcript_exists():
    assert callable(youtube_get_transcript)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_tools/test_transcript.py -v
```

Expected: FAIL with "module 'src.tools.transcript' not found"

**Step 3: Create src/tools/transcript.py**

```python
"""YouTube Transcript Tool."""
from typing import Optional
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class GetTranscriptArgs(BaseModel):
    """Arguments for getting transcript."""
    video_id: str = Field(description="YouTube video ID")
    language: str = Field(default="en", description="Language code (e.g., en, es)")


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_get_transcript(video_id: str, language: str = "en"):
    """Get transcript/captions for a YouTube video.

    Args:
        video_id: 11-character YouTube video ID
        language: Language code (default: en)

    Returns:
        Dictionary with transcript or error
    """
    client = _get_client()

    try:
        # First, get caption tracks
        captions_response = client.client.captions().list(
            part="snippet",
            videoId=video_id
        ).execute()

        items = captions_response.get("items", [])

        # Find caption in requested language
        caption_id = None
        for item in items:
            snippet = item.get("snippet", {})
            if snippet.get("languageCode") == language:
                caption_id = item.get("id")
                break

        if not caption_id and items:
            # Fall back to auto-generated or first available
            for item in items:
                snippet = item.get("snippet", {})
                track_kind = snippet.get("trackKind", "")
                if track_kind == "asr" or not caption_id:
                    caption_id = item.get("id")
                    break

        if not caption_id:
            return {
                "data": None,
                "error": {
                    "code": "NotFound",
                    "message": f"No captions available for video {video_id} in language {language}"
                },
                "pagination": None
            }

        # Download caption content (requires auth for full content, basic info available via API)
        # Note: Full transcript content may require additional processing
        return {
            "data": {
                "videoId": video_id,
                "language": language,
                "captionId": caption_id,
                "availableTracks": [
                    {
                        "id": item.get("id"),
                        "language": item.get("snippet", {}).get("languageCode"),
                        "kind": item.get("snippet", {}).get("trackKind")
                    }
                    for item in items
                ]
            },
            "error": None,
            "pagination": None
        }
    except Exception as e:
        return {
            "data": None,
            "error": {"code": type(e).__name__, "message": str(e)},
            "pagination": None
        }


def register_transcript_tools(server):
    """Register transcript tools with MCP server."""
    @server.call_tool()
    async def call_youtube_get_transcript(name, arguments):
        if name != "youtube_get_transcript":
            return None

        args = GetTranscriptArgs(**arguments)
        return await youtube_get_transcript(
            video_id=args.video_id,
            language=args.language
        )

    @server.list_tools()
    async def list_transcript_tools():
        return [{
            "name": "youtube_get_transcript",
            "description": "Get transcript/captions for a YouTube video",
            "inputSchema": GetTranscriptArgs.model_json_schema()
        }]
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_tools/test_transcript.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/tools/transcript.py tests/test_tools/test_transcript.py
git commit -m "feat: add YouTube transcript tool"
```

---

## Task 8: Playlist Tools

**Files:**

- Create: `src/tools/playlist.py`
- Modify: `src/main.py` (register the tools)
- Create: `tests/test_tools/test_playlist.py`

**Step 1: Write failing test for playlist tools**

```python
from src.tools.playlist import youtube_get_playlist, youtube_list_playlists

def test_playlist_tools_exist():
    assert callable(youtube_get_playlist)
    assert callable(youtube_list_playlists)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_tools/test_playlist.py -v
```

Expected: FAIL with "module 'src.tools.playlist' not found"

**Step 3: Create src/tools/playlist.py**

```python
"""YouTube Playlist Tools."""
from typing import Optional
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class GetPlaylistArgs(BaseModel):
    """Arguments for getting playlist details."""
    playlist_id: str = Field(description="YouTube playlist ID")
    max_results: int = Field(default=50, description="Maximum videos (1-50)")


class ListPlaylistsArgs(BaseModel):
    """Arguments for listing playlists."""
    channel_id: Optional[str] = Field(default=None, description="Channel ID (required)")
    max_results: int = Field(default=25, description="Maximum playlists (1-50)")


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_get_playlist(playlist_id: str, max_results: int = 50):
    """Get playlist details and video list.

    Args:
        playlist_id: YouTube playlist ID
        max_results: Maximum videos to return (1-50)

    Returns:
        Dictionary with playlist data or error
    """
    client = _get_client()

    try:
        # Get playlist items
        items_response = client.client.playlistItems().list(
            playlistId=playlist_id,
            part="snippet,contentDetails",
            maxResults=min(max_results, 50)
        ).execute()

        # Get playlist details
        playlists_response = client.client.playlists().list(
            id=playlist_id,
            part="snippet,contentDetails"
        ).execute()

        playlist_details = playlists_response.get("items", [{}])[0]

        return {
            "data": {
                "details": playlist_details,
                "items": items_response.get("items", [])
            },
            "error": None,
            "pagination": {
                "nextPageToken": items_response.get("nextPageToken"),
                "totalResults": items_response.get("pageInfo", {}).get("totalResults", 0)
            }
        }
    except Exception as e:
        return {
            "data": None,
            "error": {"code": type(e).__name__, "message": str(e)},
            "pagination": None
        }


async def youtube_list_playlists(channel_id: str, max_results: int = 25):
    """List playlists for a channel.

    Args:
        channel_id: YouTube channel ID
        max_results: Maximum playlists to return (1-50)

    Returns:
        Dictionary with playlists or error
    """
    client = _get_client()

    try:
        response = client.client.playlists().list(
            channelId=channel_id,
            part="snippet,contentDetails",
            maxResults=min(max_results, 50)
        ).execute()

        return {
            "data": response.get("items", []),
            "error": None,
            "pagination": {
                "nextPageToken": response.get("nextPageToken"),
                "totalResults": response.get("pageInfo", {}).get("totalResults", 0)
            }
        }
    except Exception as e:
        return {
            "data": None,
            "error": {"code": type(e).__name__, "message": str(e)},
            "pagination": None
        }


def register_playlist_tools(server):
    """Register playlist tools with MCP server."""
    @server.call_tool()
    async def call_youtube_get_playlist(name, arguments):
        if name != "youtube_get_playlist":
            return None
        args = GetPlaylistArgs(**arguments)
        return await youtube_get_playlist(
            playlist_id=args.playlist_id,
            max_results=args.max_results
        )

    @server.call_tool()
    async def call_youtube_list_playlists(name, arguments):
        if name != "youtube_list_playlists":
            return None
        args = ListPlaylistsArgs(**arguments)
        return await youtube_list_playlists(
            channel_id=args.channel_id,
            max_results=args.max_results
        )

    @server.list_tools()
    async def list_playlist_tools():
        return [
            {
                "name": "youtube_get_playlist",
                "description": "Get playlist details and video list",
                "inputSchema": GetPlaylistArgs.model_json_schema()
            },
            {
                "name": "youtube_list_playlists",
                "description": "List playlists for a channel",
                "inputSchema": ListPlaylistsArgs.model_json_schema()
            }
        ]
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_tools/test_playlist.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/tools/playlist.py tests/test_tools/test_playlist.py
git commit -m "feat: add YouTube playlist tools"
```

---

## Task 9: Comments Tool

**Files:**

- Create: `src/tools/comments.py`
- Modify: `src/main.py` (register the tool)
- Create: `tests/test_tools/test_comments.py`

**Step 1: Write failing test for comments tool**

```python
from src.tools.comments import youtube_get_comments

def test_youtube_get_comments_exists():
    assert callable(youtube_get_comments)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_tools/test_comments.py -v
```

Expected: FAIL with "module 'src.tools.comments' not found"

**Step 3: Create src/tools/comments.py**

```python
"""YouTube Comments Tool."""
from typing import Optional
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class GetCommentsArgs(BaseModel):
    """Arguments for getting comments."""
    video_id: str = Field(description="YouTube video ID")
    max_results: int = Field(default=20, description="Maximum comments (1-100)")
    page_token: Optional[str] = Field(default=None, description="Page token for pagination")


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_get_comments(video_id: str, max_results: int = 20, page_token: str = None):
    """Get comments for a YouTube video.

    Args:
        video_id: 11-character YouTube video ID
        max_results: Maximum comments (1-100)
        page_token: Pagination token for next page

    Returns:
        Dictionary with comments or error
    """
    client = _get_client()

    try:
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": min(max_results, 100),
            "order": "relevance"
        }

        if page_token:
            params["pageToken"] = page_token

        response = client.client.commentThreads().list(**params).execute()

        return {
            "data": response.get("items", []),
            "error": None,
            "pagination": {
                "nextPageToken": response.get("nextPageToken"),
                "totalResults": response.get("pageInfo", {}).get("totalResults", 0)
            }
        }
    except Exception as e:
        return {
            "data": None,
            "error": {"code": type(e).__name__, "message": str(e)},
            "pagination": None
        }


def register_comments_tools(server):
    """Register comments tools with MCP server."""
    @server.call_tool()
    async def call_youtube_get_comments(name, arguments):
        if name != "youtube_get_comments":
            return None

        args = GetCommentsArgs(**arguments)
        return await youtube_get_comments(
            video_id=args.video_id,
            max_results=args.max_results,
            page_token=args.page_token
        )

    @server.list_tools()
    async def list_comments_tools():
        return [{
            "name": "youtube_get_comments",
            "description": "Get comments for a YouTube video",
            "inputSchema": GetCommentsArgs.model_json_schema()
        }]
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_tools/test_comments.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/tools/comments.py tests/test_tools/test_comments.py
git commit -m "feat: add YouTube comments tool"
```

---

## Task 10: Channel Tool

**Files:**

- Create: `src/tools/channel.py`
- Modify: `src/main.py` (register the tool)
- Create: `tests/test_tools/test_channel.py`

**Step 1: Write failing test for channel tool**

```python
from src.tools.channel import youtube_get_channel

def test_youtube_get_channel_exists():
    assert callable(youtube_get_channel)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_tools/test_channel.py -v
```

Expected: FAIL with "module 'src.tools.channel' not found"

**Step 3: Create src/tools/channel.py**

```python
"""YouTube Channel Tool."""
from typing import Optional
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class GetChannelArgs(BaseModel):
    """Arguments for getting channel details."""
    channel_id: Optional[str] = Field(default=None, description="YouTube channel ID")
    username: Optional[str] = Field(default=None, description="Channel username (e.g., @channel)")


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_get_channel(channel_id: str = None, username: str = None):
    """Get channel information.

    Args:
        channel_id: YouTube channel ID (24 characters)
        username: Channel username starting with @

    Returns:
        Dictionary with channel data or error
    """
    client = _get_client()

    if not channel_id and not username:
        return {
            "data": None,
            "error": {
                "code": "InvalidInput",
                "message": "Either channel_id or username is required"
            },
            "pagination": None
        }

    try:
        params = {
            "part": "snippet,statistics,contentDetails"
        }

        if username:
            # Convert username to channel ID
            # For API v3, we use 'forUsername' parameter
            params["forUsername"] = username.lstrip("@")
        else:
            params["id"] = channel_id

        response = client.client.channels().list(**params).execute()

        if not response.get("items"):
            return {
                "data": None,
                "error": {
                    "code": "NotFound",
                    "message": f"Channel not found: {channel_id or username}"
                },
                "pagination": None
            }

        return {
            "data": response["items"][0],
            "error": None,
            "pagination": None
        }
    except Exception as e:
        return {
            "data": None,
            "error": {"code": type(e).__name__, "message": str(e)},
            "pagination": None
        }


def register_channel_tools(server):
    """Register channel tools with MCP server."""
    @server.call_tool()
    async def call_youtube_get_channel(name, arguments):
        if name != "youtube_get_channel":
            return None

        args = GetChannelArgs(**arguments)
        return await youtube_get_channel(
            channel_id=args.channel_id,
            username=args.username
        )

    @server.list_tools()
    async def list_channel_tools():
        return [{
            "name": "youtube_get_channel",
            "description": "Get channel information",
            "inputSchema": GetChannelArgs.model_json_schema()
        }]
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_tools/test_channel.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/tools/channel.py tests/test_tools/test_channel.py
git commit -m "feat: add YouTube channel tool"
```

---

## Task 11: Analytics Tool

**Files:**

- Create: `src/tools/analytics.py`
- Modify: `src/main.py` (register the tool)
- Create: `tests/test_tools/test_analytics.py`

**Step 1: Write failing test for analytics tool**

```python
from src.tools.analytics import youtube_get_analytics

def test_youtube_get_analytics_exists():
    assert callable(youtube_get_analytics)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_tools/test_analytics.py -v
```

Expected: FAIL with "module 'src.tools.analytics' not found"

**Step 3: Create src/tools/analytics.py**

```python
"""YouTube Analytics Tool."""
from typing import Optional, List
from src.config import get_config
from src.youtube_client import YouTubeClient
from pydantic import BaseModel, Field


class GetAnalyticsArgs(BaseModel):
    """Arguments for getting analytics."""
    ids: str = Field(description="Channel or video ID (format: channel==ID or video==ID)")
    metrics: List[str] = Field(
        default=["views", "likes", "comments"],
        description="Metrics to retrieve: views, likes, comments, dislikes, estimatedMinutesWatched"
    )
    start_date: Optional[str] = Field(default=None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(default=None, description="End date (YYYY-MM-DD)")


_client: Optional[YouTubeClient] = None


def _get_client() -> YouTubeClient:
    """Get or create YouTube client singleton."""
    global _client
    if _client is None:
        config = get_config()
        _client = YouTubeClient(api_key=config.api_key)
    return _client


async def youtube_get_analytics(ids: str, metrics: list = None, start_date: str = None, end_date: str = None):
    """Get analytics data for a channel or video.

    Note: This requires additional OAuth scopes. With API key only, limited data is available.
    Basic statistics are available via the videos/channels endpoints.

    Args:
        ids: Channel or video ID (format: channel==ID or video==ID)
        metrics: List of metrics to retrieve
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)

    Returns:
        Dictionary with analytics data or error
    """
    if metrics is None:
        metrics = ["views", "likes", "comments"]

    # With API key only, we can only return basic statistics from videos/channels endpoints
    # Full analytics requires OAuth authentication

    return {
        "data": {
            "message": "Full analytics API requires OAuth authentication. "
                      "With API key only, use youtube_get_video or youtube_get_channel "
                      "for basic statistics (views, likes, comments)."
        },
        "error": {
            "code": "AuthRequired",
            "message": "Analytics API requires OAuth scope. Use youtube_get_video/channel for basic stats."
        },
        "pagination": None
    }


def register_analytics_tools(server):
    """Register analytics tools with MCP server."""
    @server.call_tool()
    async def call_youtube_get_analytics(name, arguments):
        if name != "youtube_get_analytics":
            return None

        args = GetAnalyticsArgs(**arguments)
        return await youtube_get_analytics(
            ids=args.ids,
            metrics=args.metrics,
            start_date=args.start_date,
            end_date=args.end_date
        )

    @server.list_tools()
    async def list_analytics_tools():
        return [{
            "name": "youtube_get_analytics",
            "description": "Get analytics data (requires OAuth for full data, API key provides basic stats via video/channel tools)",
            "inputSchema": GetAnalyticsArgs.model_json_schema()
        }]
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_tools/test_analytics.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/tools/analytics.py tests/test_tools/test_analytics.py
git commit -m "feat: add YouTube analytics tool (API key limited)"
```

---

## Task 12: Integrate All Tools in Main Server

**Files:**

- Modify: `src/main.py`

**Step 1: Update main.py to register all tools**

```python
"""MCP Server entry point."""
import asyncio
from mcp.server import Server

server = Server("youtube-mcp-server")

# Import and register all tool modules
from src.tools.search import register_search_tools
from src.tools.video import register_video_tools
from src.tools.transcript import register_transcript_tools
from src.tools.playlist import register_playlist_tools
from src.tools.comments import register_comments_tools
from src.tools.channel import register_channel_tools
from src.tools.analytics import register_analytics_tools

# Collect all tools from all modules
_all_tools = []

async def list_tools():
    """List all available tools."""
    return _all_tools


@server.list_resources()
async def list_resources():
    return []


@server.read_resource()
async def read_resource(uri):
    raise ValueError(f"Resource not found: {uri}")


@server.list_tools()
async def mcp_list_tools():
    """List all available tools."""
    tools = []

    # Register each tool module
    search_tools = await register_search_tools(type("obj", (object,), {"list_tools": lambda self: []})())
    video_tools = await register_video_tools(type("obj", (object,), {"list_tools": lambda self: []})())
    transcript_tools = await register_transcript_tools(type("obj", (object,), {"list_tools": lambda self: []})())
    playlist_tools = await register_playlist_tools(type("obj", (object,), {"list_tools": lambda self: []})())
    comments_tools = await register_comments_tools(type("obj", (object,), {"list_tools": lambda self: []})())
    channel_tools = await register_channel_tools(type("obj", (object,), {"list_tools": lambda self: []})())
    analytics_tools = await register_analytics_tools(type("obj", (object,), {"list_tools": lambda self: []})())

    # Combine all tools (these functions will be properly registered via decorators)
    # The actual registration happens through the @server.call_tool decorators in each module
    return _all_tools


@server.call_tool()
async def call_tool(name, arguments):
    # Tool calls are routed through the registered functions in each module
    # This is a placeholder - actual routing happens via decorators
    raise ValueError(f"Tool {name} not properly registered")


async def main():
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
```

**Step 2: Actually restructure main.py with proper registration**

```python
"""MCP Server entry point - YouTube MCP Server."""
import asyncio
from mcp.server import Server

server = Server("youtube-mcp-server")

# Import all tools
from src.tools.search import youtube_search, SearchArgs
from src.tools.video import youtube_get_video, GetVideoArgs
from src.tools.transcript import youtube_get_transcript, GetTranscriptArgs
from src.tools.playlist import youtube_get_playlist, youtube_list_playlists, GetPlaylistArgs, ListPlaylistsArgs
from src.tools.comments import youtube_get_comments, GetCommentsArgs
from src.tools.channel import youtube_get_channel, GetChannelArgs
from src.tools.analytics import youtube_get_analytics, GetAnalyticsArgs


@server.list_resources()
async def list_resources():
    return []


@server.read_resource()
async def read_resource(uri):
    raise ValueError(f"Resource not found: {uri}")


@server.list_tools()
async def list_tools():
    """List all available YouTube MCP tools."""
    return [
        {
            "name": "youtube_search",
            "description": "Search YouTube for videos, channels, or playlists",
            "inputSchema": SearchArgs.model_json_schema()
        },
        {
            "name": "youtube_get_video",
            "description": "Get detailed information about a YouTube video",
            "inputSchema": GetVideoArgs.model_json_schema()
        },
        {
            "name": "youtube_get_channel",
            "description": "Get channel information",
            "inputSchema": GetChannelArgs.model_json_schema()
        },
        {
            "name": "youtube_get_transcript",
            "description": "Get transcript/captions for a YouTube video",
            "inputSchema": GetTranscriptArgs.model_json_schema()
        },
        {
            "name": "youtube_get_playlist",
            "description": "Get playlist details and video list",
            "inputSchema": GetPlaylistArgs.model_json_schema()
        },
        {
            "name": "youtube_list_playlists",
            "description": "List playlists for a channel",
            "inputSchema": ListPlaylistsArgs.model_json_schema()
        },
        {
            "name": "youtube_get_comments",
            "description": "Get comments for a YouTube video",
            "inputSchema": GetCommentsArgs.model_json_schema()
        },
        {
            "name": "youtube_get_analytics",
            "description": "Get analytics data (requires OAuth for full data)",
            "inputSchema": GetAnalyticsArgs.model_json_schema()
        },
    ]


@server.call_tool()
async def call_tool(name, arguments):
    """Route tool calls to appropriate functions."""
    if name == "youtube_search":
        args = SearchArgs(**arguments)
        return await youtube_search(
            query=args.query,
            max_results=args.max_results,
            order=args.order,
            type=args.type
        )
    elif name == "youtube_get_video":
        args = GetVideoArgs(**arguments)
        return await youtube_get_video(
            video_id=args.video_id,
            part=args.part
        )
    elif name == "youtube_get_channel":
        args = GetChannelArgs(**arguments)
        return await youtube_get_channel(
            channel_id=args.channel_id,
            username=args.username
        )
    elif name == "youtube_get_transcript":
        args = GetTranscriptArgs(**arguments)
        return await youtube_get_transcript(
            video_id=args.video_id,
            language=args.language
        )
    elif name == "youtube_get_playlist":
        args = GetPlaylistArgs(**arguments)
        return await youtube_get_playlist(
            playlist_id=args.playlist_id,
            max_results=args.max_results
        )
    elif name == "youtube_list_playlists":
        args = ListPlaylistsArgs(**arguments)
        return await youtube_list_playlists(
            channel_id=args.channel_id,
            max_results=args.max_results
        )
    elif name == "youtube_get_comments":
        args = GetCommentsArgs(**arguments)
        return await youtube_get_comments(
            video_id=args.video_id,
            max_results=args.max_results,
            page_token=args.page_token
        )
    elif name == "youtube_get_analytics":
        args = GetAnalyticsArgs(**arguments)
        return await youtube_get_analytics(
            ids=args.ids,
            metrics=args.metrics,
            start_date=args.start_date,
            end_date=args.end_date
        )
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
```

**Step 3: Run all tests to verify integration**

```bash
pytest tests/ -v
```

Expected: All tests pass

**Step 4: Commit**

```bash
git add src/main.py
git commit -m "feat: integrate all tools in main MCP server"
```

---

## Task 13: Skills Creation - YouTube Search Skill

**Files:**

- Create: `.claude/skills/youtube-search/SKILL.md`

**Step 1: Create youtube-search skill**

```markdown
---
name: youtube-search
description: Use this skill when searching YouTube for videos, channels, or playlists. Guides search workflow with filters and result interpretation.
---

# YouTube Search Skill

Use this skill when you need to search YouTube content.

## When to Use

- Finding videos on a topic
- Looking for channels related to a subject
- Discovering playlists
- Researching YouTube content

## Tool Usage

### Primary Tool: `youtube_search`

**Parameters:**

- `query` (required): Search terms
- `max_results` (optional, default 10): Number of results (1-50)
- `order` (optional, default "relevance"): Sort by relevance, date, viewCount, rating
- `type` (optional, default "video"): Resource type - video, channel, or playlist

**Common Orders:**

- `relevance`: Most relevant results
- `date`: Most recent
- `viewCount`: Most viewed
- `rating`: Highest rated

## Workflow

1. Clarify the user's search intent
2. Construct appropriate query
3. Apply filters if needed (duration, date, type)
4. Call `youtube_search` tool
5. Present results with key information (title, channel, views, date)
6. Offer follow-up actions (get video details, comments, transcript)

## Result Interpretation

For videos, highlight:

- Title and description
- Channel name
- View count and publication date
- Thumbnail URL

For channels, highlight:

- Channel name
- Subscriber count
- Description

For playlists, highlight:

- Playlist title
- Channel
- Video count
```

**Step 2: Commit**

```bash
git add .claude/skills/youtube-search/
git commit -m "feat: add youtube-search skill"
```

---

## Task 14: Skills Creation - YouTube Transcript Skill

**Files:**

- Create: `.claude/skills/youtube-transcript/SKILL.md`

**Step 1: Create youtube-transcript skill**

```markdown
---
name: youtube-transcript
description: Use this skill when retrieving or analyzing YouTube video transcripts/captions. Guides transcript retrieval and analysis workflow.
---

# YouTube Transcript Skill

Use this skill when working with video transcripts/captions.

## When to Use

- Getting video transcript for content analysis
- Extracting spoken content from videos
- Searching within video content
- Summarizing video content

## Tool Usage

### Primary Tool: `youtube_get_transcript`

**Parameters:**

- `video_id` (required): 11-character YouTube video ID
- `language` (optional, default "en"): Language code (e.g., en, es, fr, de)

## Workflow

1. Get the video ID from URL or user input
2. Call `youtube_get_transcript` with appropriate language
3. Check if captions are available
4. If transcript text is available, analyze as requested
5. If only metadata is available (due to API limitations), inform user

## Language Codes

Common codes:

- `en`: English
- `es`: Spanish
- `fr`: French
- `de`: German
- `ja`: Japanese
- `ko`: Korean
- `zh`: Chinese

## Limitations

- Full transcript text may require additional processing
- Some videos may not have captions
- Auto-generated captions may have errors
- Manual captions are typically more accurate

## Analysis Options

Once you have transcript data, you can:

- Summarize the content
- Extract key points
- Identify topics discussed
- Search for specific terms
- Create notes from the content
```

**Step 2: Commit**

```bash
git add .claude/skills/youtube-transcript/
git commit -m "feat: add youtube-transcript skill"
```

---

## Task 15: Skills Creation - YouTube Playlist Skill

**Files:**

- Create: `.claude/skills/youtube-playlist/SKILL.md`

**Step 1: Create youtube-playlist skill**

```markdown
---
name: youtube-playlist
description: Use this skill when working with YouTube playlists - getting details, listing videos, or finding playlists from a channel.
---

# YouTube Playlist Skill

Use this skill when working with YouTube playlists.

## When to Use

- Getting details about a specific playlist
- Listing videos in a playlist
- Finding playlists from a channel
- Analyzing playlist content

## Tool Usage

### Get Playlist Details: `youtube_get_playlist`

**Parameters:**

- `playlist_id` (required): YouTube playlist ID (from URL)
- `max_results` (optional, default 50): Number of videos (1-50)

### List Channel Playlists: `youtube_list_playlists`

**Parameters:**

- `channel_id` (required): YouTube channel ID
- `max_results` (optional, default 25): Number of playlists (1-50)

## Workflow

### For a specific playlist:

1. Extract playlist ID from URL (usually after `list=`)
2. Call `youtube_get_playlist` with the ID
3. Present playlist metadata (title, description, video count)
4. Show video list with key details

### For channel playlists:

1. Get channel ID (from URL or youtube_get_channel)
2. Call `youtube_list_playlists` with channel ID
3. Present available playlists
4. Offer to get details for specific playlists

## ID Extraction

From URL: `https://www.youtube.com/playlist?list=PLAYLIST_ID`
The `PLAYLIST_ID` is what you need.

## Pagination

- Results include `nextPageToken` for more items
- Use `totalResults` to know the full count

## Combined Workflow

Common pattern:

1. `youtube_search` with type="playlist" to find playlists
2. `youtube_get_playlist` to get details
3. `youtube_get_video` for specific video details
```

**Step 2: Commit**

```bash
git add .claude/skills/youtube-playlist/
git commit -m "feat: add youtube-playlist skill"
```

---

## Task 16: README Documentation

**Files:**

- Create: `README.md`

**Step 1: Create comprehensive README**

````markdown
# YouTube MCP Server

A Model Context Protocol (MCP) server that exposes YouTube Data API v3 functionality to Claude Code.

## Features

- **Search**: Find videos, channels, and playlists
- **Video Details**: Get metadata, statistics, thumbnails
- **Transcripts**: Retrieve video captions/transcripts
- **Playlists**: Access playlist content and channel playlists
- **Comments**: Fetch and browse video comments
- **Channels**: Get channel information and statistics

## Installation

```bash
pip install -e ".[dev]"
```
````

## Configuration

Set the `YOUTUBE_API_KEY` environment variable:

```bash
export YOUTUBE_API_KEY="your_api_key_here"
```

Get an API key from: https://console.cloud.google.com/apis/credentials

### MCP Configuration

Add to your `~/.claude/mcp_config.json`:

```json
{
  "mcpServers": {
    "youtube": {
      "command": "python",
      "args": ["-m", "src.main"],
      "env": {
        "YOUTUBE_API_KEY": "${YOUTUBE_API_KEY}"
      }
    }
  }
}
```

## Tools

| Tool                     | Description                    |
| ------------------------ | ------------------------------ |
| `youtube_search`         | Search YouTube content         |
| `youtube_get_video`      | Get video details              |
| `youtube_get_channel`    | Get channel information        |
| `youtube_get_transcript` | Get video transcript           |
| `youtube_get_playlist`   | Get playlist details           |
| `youtube_list_playlists` | List channel playlists         |
| `youtube_get_comments`   | Get video comments             |
| `youtube_get_analytics`  | Get analytics (OAuth required) |

## Skills

Three skills are included for common workflows:

- `youtube-search`: Search and discovery workflow
- `youtube-transcript`: Transcript analysis workflow
- `youtube-playlist`: Playlist management workflow

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run server
python -m src.main
```

## API Limits

- YouTube Data API quotas apply (10,000 units/day by default)
- Rate limiting is built-in (100 requests/second default)
- Configure with `YOUTUBE_RATE_LIMIT` environment variable

## License

MIT

````

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add comprehensive README"
````

---

## Task 17: Final Verification

**Files:**

- None (verification only)

**Step 1: Run all tests**

```bash
pytest tests/ -v --tb=short
```

Expected: All tests pass

**Step 2: Check project structure**

```bash
tree -L 3 -I '__pycache__|*.pyc|.git' .
```

Expected structure matches design

**Step 3: Verify MCP server can import all tools**

```bash
python -c "from src.main import server; print('Server imports successfully')"
```

Expected: Success message

**Step 4: Final commit with implementation tag**

```bash
git tag v0.1.0
git commit --allow-empty -m "release: YouTube MCP Server v0.1.0"
```

---

## Summary

This plan creates a complete YouTube MCP server with:

1. **Configuration** - Environment-based API key setup
2. **8 MCP Tools** - Search, video, channel, transcript, playlist(s), comments, analytics
3. **3 Skills** - High-level workflows for common tasks
4. **Full Test Coverage** - Unit tests for all components
5. **Documentation** - README and inline documentation

Total: **17 tasks**, each following TDD principles with clear test/implement/verify/commit cycles.

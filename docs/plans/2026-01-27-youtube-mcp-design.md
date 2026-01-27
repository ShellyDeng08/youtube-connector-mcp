# YouTube MCP Server Design

## Overview

A comprehensive YouTube MCP server and Skills toolkit that exposes YouTube Data API v3 functionality to Claude Code. Built with Python for ease of use and fast development.

## Requirements

| Category | Details |
|----------|---------|
| **Purpose** | Comprehensive toolkit for YouTube integration |
| **Features** | Search & video info, Transcripts/captions, Playlists & comments, Analytics |
| **Auth** | API Key only (read-only access) |
| **Language** | Python |

---

## Architecture

### Overall Architecture

Three-layer architecture:

1. **MCP Layer** - Implements Model Context Protocol via stdio, translates tool requests into API calls
2. **YouTube API Layer** - Wraps YouTube Data API v3 using `google-api-python-client`
3. **Skill Layer** - High-level workflows for common YouTube tasks

### Project Structure

```
youtube-mcp-server/
├── .claude/
│   └── skills/
│       ├── youtube-search/          # Search workflow skill
│       ├── youtube-transcript/      # Transcript analysis skill
│       └── youtube-playlist/        # Playlist management skill
├── src/
│   ├── __init__.py
│   ├── main.py                      # MCP server entry point
│   ├── youtube_client.py            # YouTube API wrapper
│   ├── tools/                       # MCP tool implementations
│   │   ├── __init__.py
│   │   ├── search.py
│   │   ├── video.py
│   │   ├── transcript.py
│   │   ├── playlist.py
│   │   └── analytics.py
│   └── models/                      # Pydantic models
│       ├── __init__.py
│       └── schemas.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Test fixtures (mocked API client)
│   ├── test_tools/                  # Tool tests
│   └── test_client.py               # Client tests
├── pyproject.toml                   # Dependencies & config
├── requirements.txt
└── README.md
```

---

## MCP Tools

### Search & Discovery

| Tool | Description |
|------|-------------|
| `youtube_search` | Search videos, channels, playlists with filters (duration, date, type) |
| `youtube_get_video` | Get detailed video metadata, statistics, thumbnails |
| `youtube_get_channel` | Get channel info, subscriber count, upload playlists |
| `youtube_list_videos` | List videos from a playlist or channel uploads |

### Content Analysis

| Tool | Description |
|------|-------------|
| `youtube_get_transcript` | Retrieve video transcript/captions in specified language |
| `youtube_get_comments` | Fetch comments for a video (with pagination) |

### Playlist Management

| Tool | Description |
|------|-------------|
| `youtube_get_playlist` | Get playlist details and video list |
| `youtube_list_playlists` | List user's or channel's playlists |

### Analytics

| Tool | Description |
|------|-------------|
| `youtube_get_analytics` | Get channel or video analytics (requires read-only scope) |

---

## Data Flow

```
Claude Tool Request
       ↓
Input Validation
       ↓
YouTube API Client
       ↓
API Response Parsing
       ↓
MCP Response Format
       ↓
Claude
```

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| **Quota Exceeded** | Friendly message with quota limits (10,000 units/day) |
| **Invalid ID** | Validate before API call, clear error for malformed input |
| **Not Found** | Graceful 404 handling with resource type |
| **Network Errors** | Retry up to 3 times with exponential backoff |
| **Transcript Unavailable** | Specific message when captions don't exist |

### Rate Limiting

- Built-in rate limiter respects YouTube API quotas (100 requests/second default)
- Configurable via `YOUTUBE_RATE_LIMIT` environment variable
- Returns 429 status when approaching quota

### Response Format

```json
{
  "data": { ... },
  "error": null | { "code": ..., "message": ... },
  "pagination": {
    "nextPageToken": "...",
    "totalResults": 100
  }
}
```

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `YOUTUBE_API_KEY` | Yes | - | YouTube Data API v3 key |
| `YOUTUBE_RATE_LIMIT` | No | 100 | Max requests per second |

### MCP Configuration

```json
// ~/.claude/mcp_config.json or .mcp.json
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

---

## Testing Strategy

| Type | Tool | Description |
|------|------|-------------|
| **Unit Tests** | pytest | Mock API responses with `responses` library |
| **Integration Tests** | pytest | Optional real API tests with `TEST_YOUTUBE_API_KEY` |
| **Error Coverage** | pytest | All error paths (quota, 404, invalid ID) |

---

## Skills

### youtube-search
Guides search workflow with filters and result interpretation.

### youtube-transcript
Transcript retrieval and analysis workflow.

### youtube-playlist
Playlist discovery and management workflow.

---

## Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.10"
mcp = "^1.0.0"
google-api-python-client = "^2.140.0"
pydantic = "^2.0.0"

[tool.poetry.dev-dependencies]
pytest = "^8.0.0"
responses = "^0.25.0"
```

---

## Next Steps

1. Set up for implementation with git worktree
2. Create detailed implementation plan
3. Build MCP server
4. Create Skills

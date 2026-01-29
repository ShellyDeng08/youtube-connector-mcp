# Testing Plan - YouTube MCP Server

**Date:** 2026-01-28

## Overview

Comprehensive testing strategy for YouTube MCP Server including unit tests, MCP protocol compliance tests, and integration tests with real YouTube API calls.

## Current State

### Existing Tests
- 12 basic tests pass (imports, config, client initialization)
- Tests are mostly "existence checks" - verify functions can be imported
- No actual API interaction tests
- No error handling tests
- No MCP protocol compliance tests

### Issues Identified

1. **Missing dependencies** - Tests fail outside venv
2. **test_mcp.py bug** - `Server` not imported
3. **Singleton client pattern** - Test isolation issues
4. **No integration tests** - No real API calls
5. **No MCP protocol tests** - No schema validation

## Test Architecture

### Directory Structure

```
tests/
├── conftest.py           (enhance)
├── test_client.py        (expand)
├── test_config.py        (keep as-is)
├── test_imports.py       (keep as-is)
├── test_mcp_protocol.py  (NEW)
├── test_integration.py   (NEW)
├── mocks/                (NEW - mock API responses)
│   ├── responses.py
│   └── fixtures.py
└── test_tools/
    ├── test_search.py    (expand)
    ├── test_video.py     (expand)
    ├── test_channel.py   (expand)
    ├── test_comments.py  (expand)
    ├── test_playlist.py  (expand)
    ├── test_transcript.py (expand)
    └── test_analytics.py (expand)
```

### Testing Approaches

#### 1. Unit Tests (with `responses` library)
- Mock HTTP requests to YouTube API
- Test success paths, error paths, edge cases
- Isolate each tool independently
- Run fast, no API key needed
- Marked with `@pytest.mark.unit`

#### 2. MCP Protocol Tests
- Validate tool schemas are valid JSON Schema
- Verify tool names and descriptions match spec
- Test response structure: `{data, error, pagination}`
- Test `call_tool()` routing in main.py
- Marked with `@pytest.mark.mcp`

#### 3. Integration Tests (with real API key)
- Use actual YouTube API key
- Test with known good video/channel/playlist IDs
- Verify real API responses are parsed correctly
- Test pagination, rate limiting, quota errors
- Marked with `@pytest.mark.integration`

## Test Cases

### Unit Tests

**youtube_search:**
- Success: returns results with data, no error
- Success: max_results capped at 50
- Success: order parameter passed through
- Success: type parameter (video/channel/playlist)
- Error: API exception caught and formatted
- Edge: empty query handled
- Edge: pagination token preserved

**youtube_get_video:**
- Success: returns video with snippet, statistics, contentDetails
- Success: custom part parameter works
- Success: default part parameter used
- Error: video not found returns custom NotFound error
- Error: API exception caught
- Edge: invalid video_id format

**youtube_get_channel:**
- Success: channel by ID
- Success: channel by username (strips @ prefix)
- Error: neither ID nor username provided returns InvalidInput
- Error: channel not found returns NotFound
- Error: API exception caught

**youtube_get_transcript:**
- Success: finds caption in requested language
- Success: falls back to auto-generated (asr) if no exact match
- Success: falls back to first available if no ASR
- Error: no captions available returns NotFound
- Error: API exception caught
- Success: returns list of all available tracks

**youtube_get_playlist:**
- Success: returns details and items
- Success: max_results capped at 50
- Success: pagination token preserved
- Error: playlist not found (handled by API)
- Error: API exception caught

**youtube_list_playlists:**
- Success: returns list of playlists
- Success: max_results capped at 50
- Success: pagination token preserved
- Error: API exception caught

**youtube_get_comments:**
- Success: returns comments
- Success: max_results capped at 100
- Success: page_token passed through
- Success: defaults to order=relevance
- Error: API exception caught

**youtube_get_analytics:**
- Always returns AuthRequired error message
- Validates that error code is "AuthRequired"
- Suggests using youtube_get_video/channel for basic stats

### MCP Protocol Tests

**Schema validation:**
- Each tool's `model_json_schema()` is valid JSON Schema
- Required fields are marked correctly
- Default values match function defaults
- Descriptions exist for all fields

**Tool registration in main.py:**
- `list_tools()` returns exactly 8 tools
- Each tool has: name, description, inputSchema
- Tool names match: `youtube_search`, `youtube_get_video`, etc.
- No duplicate tool names

**call_tool() routing:**
- Each tool routes to correct function
- Arguments are parsed with correct Pydantic model
- Unknown tool name raises ValueError

**Response structure:**
- All successful responses have: `data`, `error: None`, optional `pagination`
- All error responses have: `data: None`, `error: {code, message}`, `pagination: None`
- Error codes are strings (not Python exception classes)

### Integration Tests

**Happy path tests:**
- Search for "Python tutorial" → returns videos
- Get video details for a known video ID
- Get channel by ID → returns channel stats
- Get playlist contents → returns videos
- Get comments for a video → returns comment threads

**Pagination tests:**
- Search returns `nextPageToken` when > max_results
- Using `page_token` retrieves next page
- Playlist items support pagination

**Rate limiting tests:**
- Multiple requests in sequence work
- Quota exceeded error is caught and formatted

**Data format validation:**
- Video statistics include: viewCount, likeCount, commentCount
- Channel statistics include: subscriberCount, videoCount
- Response dates are ISO 8601 format

## Implementation Plan

### Phase 1: Fix Immediate Issues

1. **Fix test_mcp.py**
   - Add `from mcp.server import Server` import
   - Verify script runs successfully

2. **Enhance conftest.py**
   - Add mock API response fixtures
   - Add test video/channel/playlist IDs
   - Add fixture to skip integration tests without API key

3. **Add pytest marks**
   - `@pytest.mark.unit` - unit tests with mocks
   - `@pytest.mark.integration` - real API tests
   - `@pytest.mark.mcp` - protocol tests

### Phase 2: Unit Tests Expansion

For each tool file, add `responses` mocked HTTP responses for:
- Success case with valid YouTube API response
- 404 Not Found
- 403 Forbidden (quota exceeded)
- 400 Bad Request
- Network timeout

### Phase 3: MCP Protocol Tests

Create `test_mcp_protocol.py` covering schema validation and response format.

### Phase 4: Integration Tests

Create `test_integration.py` with real API calls using test data.

### Phase 5: Dependencies

Add to `pyproject.toml`:
```toml
[tool.poetry.dev-dependencies]
pytest = "^8.0.0"
responses = "^0.25.0"
pytest-cov = "^6.0.0"
pytest-mock = "^3.14.0"
```

## Test Execution

### Run unit tests only
```bash
pytest -m unit tests/ -v
```

### Run integration tests (requires API key)
```bash
YOUTUBE_API_KEY_TEST=your_key pytest -m integration tests/ -v
```

### Run all tests
```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Coverage Target
- Minimum 80% code coverage
- 100% coverage for critical paths (error handling)

## Tools Summary

| Tool | Description | Test Focus |
|------|-------------|------------|
| `youtube_search` | Search videos, channels, playlists | Pagination, filters |
| `youtube_get_video` | Get video details | Part parameter, not found |
| `youtube_get_channel` | Get channel info | ID vs username, validation |
| `youtube_get_transcript` | Get video captions | Language fallback, no captions |
| `youtube_get_playlist` | Get playlist contents | Pagination, nested responses |
| `youtube_list_playlists` | List channel playlists | Pagination |
| `youtube_get_comments` | Get video comments | Pagination, order |
| `youtube_get_analytics` | Get analytics (OAuth) | Error message, suggestion |

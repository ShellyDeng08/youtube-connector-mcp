# YouTube MCP Server

<div align="center">

**Connect Claude to YouTube Data API v3**

Search videos, get details, fetch comments, access playlists, transcripts, and more.

[![PyPI Version](https://img.shields.io/pypi/v/youtube-connector-mcp)](https://pypi.org/project/youtube-connector-mcp/)
[![Python Version](https://img.shields.io/pypi/pyversions/youtube-connector-mcp)](https://pypi.org/project/youtube-connector-mcp/)
[![License](https://img.shields.io/pypi/l/youtube-connector-mcp)](LICENSE)

**PyPI Package**: `youtube-connector-mcp`

</div>

---

## Quick Start

```bash
# 1. Get your YouTube API Key from Google Cloud Console
#    https://console.cloud.google.com/apis/credentials

# 2. Set your API key as environment variable
export YOUTUBE_API_KEY="your_api_key_here"

# 3. Install the package
pip install youtube-connector-mcp

# 4. Add the MCP server
claude mcp add -s user -e YOUTUBE_API_KEY="${YOUTUBE_API_KEY}" youtube-connector-mcp -- youtube-connector-mcp

# 5. Restart Claude Code and start using!
```

---

## Prerequisites

| Requirement | How to Get |
|-------------|-------------|
| **Python 3.10+** | [Download Python](https://www.python.org/downloads/) or `brew install python3` |
| **YouTube API Key** | Get it free from [Google Cloud Console](https://console.cloud.google.com/apis/credentials) |
| **Claude Code** | Install from [claude.com/code](https://claude.com/code) |

---

## Installation

### Install from PyPI (Recommended)

```bash
pip install youtube-connector-mcp
```

> **Note:** If `pip` doesn't work, try `pip3 install youtube-connector-mcp`

### Install from Source

```bash
git clone https://github.com/ShellyDeng08/youtube-connector-mcp.git
cd youtube-connector-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Verify Installation

```bash
youtube-connector-mcp --help
claude mcp list  # Check if server is registered
```

---

## Configuration

### Option 1: Using `claude mcp add` (Easiest)

```bash
# Install for current project only
claude mcp add -s local -e YOUTUBE_API_KEY="${YOUTUBE_API_KEY}" youtube-connector-mcp -- youtube-connector-mcp

# Install for all your projects (recommended)
claude mcp add -s user -e YOUTUBE_API_KEY="${YOUTUBE_API_KEY}" youtube-connector-mcp -- youtube-connector-mcp

# Install to project's .mcp.json
claude mcp add -s project -e YOUTUBE_API_KEY="${YOUTUBE_API_KEY}" youtube-connector-mcp -- youtube-connector-mcp
```

> **Don't have an API key?** See [Creating a YouTube API Key](#creating-a-youtube-api-key) below - it's free and takes just a few minutes.

### Option 2: Manual Configuration

Add to your `~/.claude/mcp_config.json`:

```json
{
  "mcpServers": {
    "youtube-connector-mcp": {
      "command": "youtube-connector-mcp",
      "env": {
        "YOUTUBE_API_KEY": "${YOUTUBE_API_KEY}"
      }
    }
  }
}
```

### API Key Setup

**Set as Environment Variable (Recommended):**

```bash
# Linux/Mac - Add to ~/.bashrc, ~/.zshrc, or ~/.profile
export YOUTUBE_API_KEY="your_api_key_here"
source ~/.zshrc
```

```powershell
# Windows PowerShell - Add to $PROFILE
$env:YOUTUBE_API_KEY="your_api_key_here"
# Or set permanently
[System.Environment]::SetEnvironmentVariable('YOUTUBE_API_KEY', 'your_api_key_here', 'User')
```

```cmd
# Windows CMD
setx YOUTUBE_API_KEY "your_api_key_here"
```

**Or Put Directly in MCP Config:**

```json
{
  "mcpServers": {
    "youtube-connector-mcp": {
      "command": "youtube-connector-mcp",
      "env": {
        "YOUTUBE_API_KEY": "AIzaSyC-Your-Actual-API-Key-Here"
      }
    }
  }
}
```

> **Security Note:** Using environment variables is safer as it keeps your key out of version control.

### Creating a YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable [YouTube Data API v3](https://console.cloud.google.com/apis/library)
4. Go to [Credentials](https://console.cloud.google.com/apis/credentials) and create an API key
5. (Optional) Restrict the key to YouTube Data API v3 for better security

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `YOUTUBE_API_KEY` | Yes | - | YouTube Data API v3 key |
| `YOUTUBE_RATE_LIMIT` | No | 100 | Max requests per second |

---

## Features

### Core Capabilities

| Tool | Description |
|------|-------------|
| `youtube_search` | Search videos, channels, playlists with filters (duration, date, type, order) |
| `youtube_get_video` | Get detailed video metadata, statistics, thumbnails, and content details |
| `youtube_get_channel` | Get channel info, subscriber count, upload playlists, statistics |
| `youtube_get_transcript` | Retrieve actual video transcript text with timestamps |
| `youtube_get_comments` | Fetch video comments with pagination support |
| `youtube_get_playlist` | Get playlist details and complete video list |
| `youtube_list_playlists` | List all playlists for a specific channel |
| `youtube_get_analytics` | Get analytics data (views, likes, comments, watch time) |

### Use Cases

- **Research**: Search and analyze YouTube content programmatically
- **Content Analysis**: Extract transcripts and comments for AI processing
- **Channel Monitoring**: Track channel statistics and new uploads
- **Data Mining**: Gather YouTube data for analytics projects
- **Automated Workflows**: Integrate YouTube data into Claude-assisted workflows

---

## Usage Examples

| Category | Example Prompts |
|----------|----------------|
| **Search** | "Search for Python tutorials" / "Find recent AI videos" / "Channels about cooking with 100k+ subscribers" |
| **Video** | "Get details for this video: URL" / "What's the view count?" / "Get the transcript" |
| **Channel** | "How many subscribers does @MKBHD have?" / "Recent uploads from this channel" / "Channel statistics" |
| **Playlist** | "List all playlists for this channel" / "Get videos in this playlist" |
| **Comments/Analytics** | "Get top comments for this video" / "Show channel analytics" |

---

## Troubleshooting

### MCP Server Not Found

**Error:** `No MCP servers configured`

**Solutions:**
1. Verify `~/.claude/mcp_config.json` exists
2. Check JSON syntax is valid
3. Run `claude mcp list` to see registered servers
4. Restart Claude Code after updating config

### Python Not Found

**Error:** `command not found: python`

**Solutions:**
1. Use `python3` instead of `python`
2. Provide full path: `which python3` (Mac/Linux) or `where python` (Windows)

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'mcp'`

**Solutions:**
1. Activate virtual environment: `source .venv/bin/activate`
2. Reinstall: `pip install youtube-connector-mcp`

### API Quota Exceeded

**Error:** `403 Forbidden - quota exceeded`

**Solutions:**
1. Check [Google Cloud Console quota](https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas)
2. Default: 10,000 units/day
3. Consider upgrading for higher limits

### Transcript Not Available

**Error:** "No transcript available" or "Transcripts are disabled"

**Solutions:**
1. Video may not have captions enabled
2. Auto-generated captions may take 24+ hours after upload
3. Try a video known to have captions

### Transcript Request Blocked

**Error:** "YouTube is blocking requests from your IP"

**Solutions:**
See [youtube-transcript-api documentation](https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception) for proxy options.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Links

- [GitHub Repository](https://github.com/ShellyDeng08/youtube-connector-mcp)
- [PyPI Package](https://pypi.org/project/youtube-connector-mcp/)
- [YouTube Data API v3 Docs](https://developers.google.com/youtube/v3)
- [Claude Code](https://claude.com/code)

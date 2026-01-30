# YouTube MCP Server

Connect Claude to YouTube Data API v3 - search videos, get details, fetch comments, access playlists, transcripts, and more.

---

## Prerequisites

Before you begin, make sure you have:

| Requirement | How to Get |
|-------------|-------------|
| **Python 3.10+** | [Download Python](https://www.python.org/downloads/) or install via `brew install python3` |
| **YouTube API Key** | Get it for free from [Google Cloud Console](https://console.cloud.google.com/apis/credentials) - see [API Key Setup](#api-key-setup) below |
| **Claude Code** | Install from [claude.com/code](https://claude.com/code) |

> **Important:** You need a YouTube API key to use this MCP server. Without it, the server will not work. Get your API key now following the steps below before proceeding.

---

## Table of Contents

- [Prerequisites](#prerequisites) ← **1. Start here**
- [Features](#features)
- [API Key Setup](#api-key-setup) ← **2. Do this first**
- [Installation](#installation) ← **3. Then install**
- [Configuration](#configuration) ← **4. Then configure**
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

| Tool | Description |
|-------|-------------|
| `youtube_search` | Search videos, channels, playlists with filters (duration, date, type) |
| `youtube_get_video` | Get detailed video metadata, statistics, thumbnails |
| `youtube_get_channel` | Get channel info, subscriber count, upload playlists |
| `youtube_get_transcript` | Retrieve actual video transcript text and segments (requires video to have captions enabled) |
| `youtube_get_comments` | Fetch comments for a video (with pagination) |
| `youtube_get_playlist` | Get playlist details and video list |
| `youtube_list_playlists` | List playlists for a channel |
| `youtube_get_analytics` | Get analytics data (requires OAuth for full data) |

---

## API Key Setup

> **Do this step BEFORE installing and configuring.** You need a YouTube API key to use this MCP server.

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one

### Step 2: Enable YouTube Data API v3

1. Navigate to [APIs & Services > Library](https://console.cloud.google.com/apis/library)
2. Search for "YouTube Data API v3"
3. Click "Enable"

### Step 3: Create API Credentials

1. Go to [APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" > "API key"
3. Copy your API key

### Step 4: Restrict the API Key (Recommended)

1. Click "Edit" on your API key
2. Under "Application restrictions", select "IP addresses"
3. Add your IP address (or leave open for development)
4. Under "API restrictions", select "YouTube Data API v3"

### Step 5: Use Your API Key

You have two options:

**Option A: Set as Environment Variable** (Recommended for security)

Set `YOUTUBE_API_KEY` environment variable, then use `${YOUTUBE_API_KEY}` in your MCP config:

**Linux/Mac:**

```bash
# Add to ~/.bashrc, ~/.zshrc, or ~/.profile
export YOUTUBE_API_KEY="your_api_key_here"

# Reload shell
source ~/.zshrc
```

**Windows (PowerShell):**

```powershell
# Add to $PROFILE
$env:YOUTUBE_API_KEY="your_api_key_here"

# Or set permanently
[System.Environment]::SetEnvironmentVariable('YOUTUBE_API_KEY', 'your_api_key_here', 'User')
```

**Windows (CMD):**

```cmd
setx YOUTUBE_API_KEY "your_api_key_here"
```

**Option B: Put Directly in MCP Config**

Paste your API key directly in `~/.claude/mcp_config.json`:

```json
{
  "mcpServers": {
    "youtube-mcp-server": {
      "command": "python",
      "args": ["-m", "src.main"],
      "env": {
        "YOUTUBE_API_KEY": "AIzaSyC-Your-Actual-API-Key-Here"
      }
    }
  }
}
```

> **Security Note:** Option A (environment variable) is safer as it keeps your key out of version control and config files that might be shared.

---

## Installation

```bash
# Navigate to the project directory
cd youtube-mcp-server

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Configuration

Add to your `~/.claude/mcp_config.json`:

```json
{
  "mcpServers": {
    "youtube-mcp-server": {
      "command": "/path/to/youtube-mcp-server/.venv/bin/python",
      "args": ["-m", "src.main"],
      "cwd": "/path/to/youtube-mcp-server",
      "env": {
        "YOUTUBE_API_KEY": "${YOUTUBE_API_KEY}"
      }
    }
  }
}
```

Replace `/path/to/youtube-mcp-server` with your actual path, e.g.:
`/Users/bytedance/Documents/code/youtube-mcp-server`

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `YOUTUBE_API_KEY` | Yes | - | YouTube Data API v3 key |
| `YOUTUBE_RATE_LIMIT` | No | 100 | Max requests per second (rate limiting) |

---

## Usage

Restart Claude Code and ask naturally:

> "Search for Python tutorials"
> "Summarize this video: https://youtube.com/watch?v=xxx"
> "Get the transcript for this video"
> "How many subscribers does this channel have?"

---

## Troubleshooting

### MCP Server Not Found

**Error:** `No MCP servers configured`

**Solution:**
1. Check that `~/.claude/mcp_config.json` exists
2. Verify JSON is valid (no syntax errors)
3. Restart Claude Code after updating config

### Python Not Found

**Error:** `command not found: python`

**Solution:**
1. Use `python3` instead of `python` in your config
2. Or provide the full path to your Python executable:
   ```bash
   which python3  # On Mac/Linux
   where python  # On Windows
   ```

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'mcp'`

**Solution:**
1. Ensure you installed dependencies in the correct environment
2. If using venv, activate it first: `source .venv/bin/activate`
3. Reinstall dependencies: `pip install -r requirements.txt`

### API Key Issues

**Error:** `403 Forbidden - quota exceeded`

**Solution:**
1. Check your [Google Cloud Console quota](https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas)
2. Default quota is 10,000 units per day
3. Consider upgrading your plan for higher limits

### Import Errors

**Error:** `ImportError: cannot import name '...'`

**Solution:**
1. Ensure you're running from the project root directory
2. Check that `cwd` is set correctly in MCP config
3. Verify all files exist in `src/` directory

### Permissions Issues

**Error:** `Permission denied` when installing

**Solution:**
1. Use a virtual environment (recommended)
2. Or use `pip install --user` for user-space installation
3. Or use `pip install --break-system-packages` (not recommended)

### Transcript Not Available

**Error:** "No transcript available for video" or "Transcripts are disabled"

**Solution:**
1. The video may not have captions/subtitles enabled by the creator
2. Auto-generated captions may not be available yet (can take 24+ hours after upload)
3. Try a different video that is known to have captions

### Transcript Request Blocked

**Error:** "YouTube is blocking requests from your IP"

**Solution:**
This can happen when using cloud providers or making too many requests. See the [youtube-transcript-api documentation](https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception) for proxy configuration options.

---

## License

MIT License - see LICENSE file for details.

---

## For Developers

If you want to contribute or extend this MCP server, see [DEVELOPMENT.md](docs/DEVELOPMENT.md) for:
- Running tests
- Project structure
- Adding new tools
- Building and publishing to PyPI

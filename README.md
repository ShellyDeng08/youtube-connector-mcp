# YouTube MCP Server

Connect Claude to YouTube Data API v3 - search videos, get details, fetch comments, access playlists, and more.

---

## Quick Start

### 1. Install

```bash
npx -y @your-username/youtube-mcp-server
```

### 2. Configure

Add to `~/.claude/mcp_config.json`:

```json
{
  "mcpServers": {
    "youtube": {
      "command": "python",
      "args": ["src/main.py"],
      "env": {
        "YOUTUBE_API_KEY": "${YOUTUBE_API_KEY}"
      }
    }
  }
}
```

### 3. Get API Key

Visit: https://console.cloud.google.com/apis/credentials

```bash
export YOUTUBE_API_KEY="your_api_key_here"
```

## Features

| Tool | Description |
|-------|-------------|
| `youtube_search` | Search videos, channels, playlists |
| `youtube_get_video` | Get video details, statistics |
| `youtube_get_comments` | Fetch and browse comments |
| `youtube_get_channel` | Get channel information |
| `youtube_get_playlist` | Access playlist contents |

## Usage

Just ask Claude naturally:

> "搜索关于 Claude Code 的教程视频"
> "这个视频 https://youtube.com/watch?v=dQw4w9WxXc 有多少评论？"
> "获取这个频道的订阅数"

Claude will automatically use the YouTube MCP tools.

## Development

For development instructions, see: [docs/tech-sharing-skills-plugins-mcp.md](docs/tech-sharing-skills-plugins-mcp.md)

## License

MIT

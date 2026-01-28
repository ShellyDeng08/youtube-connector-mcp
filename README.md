# YouTube MCP Server

> **这是什么？** 这是一个 **MCP 服务器**，不是 Plugin。
>
> MCP 服务器让 Claude 能访问外部 API。配置后，Claude 可以像使用内置工具一样调用 YouTube API。
>
> 安装后立即可用，无需额外配置。
>

A Model Context Protocol (MCP) server that exposes YouTube Data API v3 functionality to Claude Code.

## Features

- **Search**: Find videos, channels, and playlists with filters
- **Video Details**: Get metadata, statistics, thumbnails
- **Transcripts**: Retrieve video captions/transcripts
- **Playlists**: Access playlist content and channel playlists
- **Comments**: Fetch and browse video comments
- **Channels**: Get channel information and statistics
- **Analytics**: Basic statistics via video/channel tools (OAuth required for full data)

## Installation

### Via npm (Recommended)

\`\`\`bash
npx -y @your-username/youtube-mcp-server
\`\`\`

### Configuration

Add to your `~/.claude/mcp_config.json`:

\`\`\`json
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
\`\`\`

### Environment Variable

\`\`\`bash
export YOUTUBE_API_KEY="your_api_key_here"
\`\`\`

Get an API key from: https://console.cloud.google.com/apis/credentials

## Tools

| Tool | Description |
|-------|-------------|
| `youtube_search` | Search YouTube for videos, channels, or playlists |
| `youtube_get_video` | Get detailed information about a YouTube video |
| `youtube_get_channel` | Get channel information |
| `youtube_get_transcript` | Get transcript/captions for a YouTube video |
| `youtube_get_playlist` | Get playlist details and video list |
| `youtube_list_playlists` | List channel playlists |
| `youtube_get_comments` | Get comments for a YouTube video |
| `youtube_get_analytics` | Get analytics data (OAuth required) |

## Usage Examples

### Search Videos

\`\`\`text
User: Find Claude Code tutorial videos
\`\`\`

Claude will automatically use the `youtube_search` tool.

### Get Video Details

\`\`\`text
User: Tell me about video dQw4w9WxXcQ
\`\`\`

Claude will use `youtube_get_video` to fetch details.

### Browse Comments

\`\`\`text
User: What are people saying about this video?
\`\`\`

Claude will use `youtube_get_comments` to fetch and analyze.

## Development

\`\`\`bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run server
python src/main.py
\`\`\`

## API Limits

- YouTube Data API quotas apply (10,000 units/day by default)
- Rate limiting is built-in (100 requests/second default)
- Configure with `YOUTUBE_RATE_LIMIT` environment variable

## License

MIT

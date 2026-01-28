# YouTube MCP Server

A Model Context Protocol (MCP) server that exposes YouTube Data API v3 functionality to Claude Code.

## Features

- **Search**: Find videos, channels, and playlists
- **Video Details**: Get metadata, statistics, thumbnails
- **Transcripts**: Retrieve video captions/transcripts
- **Playlists**: Access playlist content and channel playlists
- **Comments**: Fetch and browse video comments
- **Channels**: Get channel information and statistics
- **Analytics**: Basic statistics via video/channel tools (OAuth required for full analytics)

## Installation

\`\`\`bash
pip install -e ".[dev]"
\`\`\`

## Configuration

Set \`YOUTUBE_API_KEY\` environment variable:

\`\`\`bash
export YOUTUBE_API_KEY="your_api_key_here"
\`\`\`

Get an API key from: https://console.cloud.google.com/apis/credentials

### MCP Configuration

Add to your \`~/.claude/mcp_config.json\`:

\`\`\`json
{
  "mcpServers": {
    "youtube": {
      "command": "python",
      "args": ["-m", "src.main"],
      "env": {
        "YOUTUBE_API_KEY": "\${YOUTUBE_API_KEY}"
      }
    }
  }
}
\`\`\`

## Tools

| Tool                     | Description                    |
| ------------------------ | ------------------------------ |
| \`youtube_search\`         | Search YouTube content         |
| \`youtube_get_video\`      | Get video details              |
| \`youtube_get_channel\`    | Get channel information        |
| \`youtube_get_transcript\` | Get video transcript           |
| \`youtube_get_playlist\`   | Get playlist details           |
| \`youtube_list_playlists\` | List channel playlists         |
| \`youtube_get_comments\`   | Get video comments             |
| \`youtube_get_analytics\`  | Get analytics (OAuth required) |

## Skills

Three skills are included for common workflows:

- \`youtube-search\`: Search and discovery workflow
- \`youtube-transcript\`: Transcript analysis workflow
- \`youtube-playlist\`: Playlist management workflow

## Development

\`\`\`bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run server
python -m src.main
\`\`\`

## API Limits

- YouTube Data API quotas apply (10,000 units/day by default)
- Rate limiting is built-in (100 requests/second default)
- Configure with \`YOUTUBE_RATE_LIMIT\` environment variable

## License

MIT

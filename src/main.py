"""MCP Server entry point - YouTube MCP Server."""
import asyncio
import mcp.types as types
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
        types.Tool(
            name="youtube_search",
            description="Search YouTube for videos, channels, or playlists",
            inputSchema=SearchArgs.model_json_schema()
        ),
        types.Tool(
            name="youtube_get_video",
            description="Get detailed information about a YouTube video",
            inputSchema=GetVideoArgs.model_json_schema()
        ),
        types.Tool(
            name="youtube_get_channel",
            description="Get channel information",
            inputSchema=GetChannelArgs.model_json_schema()
        ),
        types.Tool(
            name="youtube_get_transcript",
            description="Get transcript/captions for a YouTube video",
            inputSchema=GetTranscriptArgs.model_json_schema()
        ),
        types.Tool(
            name="youtube_get_playlist",
            description="Get playlist details and video list",
            inputSchema=GetPlaylistArgs.model_json_schema()
        ),
        types.Tool(
            name="youtube_list_playlists",
            description="List playlists for a channel",
            inputSchema=ListPlaylistsArgs.model_json_schema()
        ),
        types.Tool(
            name="youtube_get_comments",
            description="Get comments for a YouTube video",
            inputSchema=GetCommentsArgs.model_json_schema()
        ),
        types.Tool(
            name="youtube_get_analytics",
            description="Get analytics data (requires OAuth for full data)",
            inputSchema=GetAnalyticsArgs.model_json_schema()
        ),
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

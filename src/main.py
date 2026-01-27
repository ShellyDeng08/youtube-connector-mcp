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

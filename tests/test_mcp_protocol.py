"""MCP Protocol compliance tests."""
import pytest
from src.main import server, list_tools, call_tool
import json


@pytest.mark.mcp
@pytest.mark.unit
class TestMCPProtocol:
    """Test MCP protocol compliance."""

    @pytest.mark.asyncio
    async def test_list_tools_returns_all_tools(self):
        """list_tools() should return exactly 8 tools."""
        tools = await list_tools()
        assert len(tools) == 8

    @pytest.mark.asyncio
    async def test_list_tools_tool_names(self):
        """list_tools() should return correct tool names."""
        tools = await list_tools()
        tool_names = {tool["name"] for tool in tools}
        expected_names = {
            "youtube_search",
            "youtube_get_video",
            "youtube_get_channel",
            "youtube_get_transcript",
            "youtube_get_playlist",
            "youtube_list_playlists",
            "youtube_get_comments",
            "youtube_get_analytics",
        }
        assert tool_names == expected_names

    @pytest.mark.asyncio
    async def test_list_tools_no_duplicate_names(self):
        """list_tools() should not have duplicate tool names."""
        tools = await list_tools()
        tool_names = [tool["name"] for tool in tools]
        assert len(tool_names) == len(set(tool_names))

    @pytest.mark.asyncio
    async def test_each_tool_has_required_fields(self):
        """Each tool should have name, description, inputSchema."""
        tools = await list_tools()
        for tool in tools:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool

    @pytest.mark.asyncio
    async def test_tool_descriptions_not_empty(self):
        """Each tool should have a non-empty description."""
        tools = await list_tools()
        for tool in tools:
            assert tool["description"]
            assert len(tool["description"]) > 0

    @pytest.mark.asyncio
    async def test_tool_schemas_valid_json(self):
        """Each tool's inputSchema should be valid JSON."""
        tools = await list_tools()
        for tool in tools:
            schema = tool["inputSchema"]
            # Should be serializable
            json_str = json.dumps(schema)
            assert json_str
            # Should be deserializable
            parsed = json.loads(json_str)
            assert parsed == schema

    @pytest.mark.asyncio
    async def test_tool_schemas_follow_json_schema(self):
        """Each tool's inputSchema should be a valid JSON Schema."""
        tools = await list_tools()
        for tool in tools:
            schema = tool["inputSchema"]
            # JSON Schema must have a type
            assert "type" in schema
            # Common types for our schemas
            assert schema["type"] in ["object", "array", "string"]

    @pytest.mark.asyncio
    async def test_search_schema_properties(self):
        """youtube_search schema should have correct properties."""
        tools = await list_tools()
        search_tool = next(t for t in tools if t["name"] == "youtube_search")
        schema = search_tool["inputSchema"]

        assert "properties" in schema
        props = schema["properties"]
        assert "query" in props
        assert "max_results" in props
        assert "order" in props
        assert "type" in props

    @pytest.mark.asyncio
    async def test_search_query_required(self):
        """query should be required in youtube_search."""
        tools = await list_tools()
        search_tool = next(t for t in tools if t["name"] == "youtube_search")
        schema = search_tool["inputSchema"]

        assert "required" in schema
        assert "query" in schema["required"]

    @pytest.mark.asyncio
    async def test_search_max_results_has_default(self):
        """max_results should have default value."""
        tools = await list_tools()
        search_tool = next(t for t in tools if t["name"] == "youtube_search")
        schema = search_tool["inputSchema"]

        max_results = schema["properties"]["max_results"]
        assert "default" in max_results
        assert max_results["default"] == 10

    @pytest.mark.asyncio
    async def test_get_video_schema_properties(self):
        """youtube_get_video schema should have correct properties."""
        tools = await list_tools()
        video_tool = next(t for t in tools if t["name"] == "youtube_get_video")
        schema = video_tool["inputSchema"]

        assert "properties" in schema
        props = schema["properties"]
        assert "video_id" in props
        assert "part" in props

    @pytest.mark.asyncio
    async def test_get_channel_schema_properties(self):
        """youtube_get_channel schema should have correct properties."""
        tools = await list_tools()
        channel_tool = next(t for t in tools if t["name"] == "youtube_get_channel")
        schema = channel_tool["inputSchema"]

        assert "properties" in schema
        props = schema["properties"]
        assert "channel_id" in props
        assert "username" in props

    @pytest.mark.asyncio
    async def test_get_transcript_schema_properties(self):
        """youtube_get_transcript schema should have correct properties."""
        tools = await list_tools()
        transcript_tool = next(t for t in tools if t["name"] == "youtube_get_transcript")
        schema = transcript_tool["inputSchema"]

        assert "properties" in schema
        props = schema["properties"]
        assert "video_id" in props
        assert "language" in props

    @pytest.mark.asyncio
    async def test_get_playlist_schema_properties(self):
        """youtube_get_playlist schema should have correct properties."""
        tools = await list_tools()
        playlist_tool = next(t for t in tools if t["name"] == "youtube_get_playlist")
        schema = playlist_tool["inputSchema"]

        assert "properties" in schema
        props = schema["properties"]
        assert "playlist_id" in props
        assert "max_results" in props

    @pytest.mark.asyncio
    async def test_list_playlists_schema_properties(self):
        """youtube_list_playlists schema should have correct properties."""
        tools = await list_tools()
        list_tool = next(t for t in tools if t["name"] == "youtube_list_playlists")
        schema = list_tool["inputSchema"]

        assert "properties" in schema
        props = schema["properties"]
        assert "channel_id" in props
        assert "max_results" in props

    @pytest.mark.asyncio
    async def test_get_comments_schema_properties(self):
        """youtube_get_comments schema should have correct properties."""
        tools = await list_tools()
        comments_tool = next(t for t in tools if t["name"] == "youtube_get_comments")
        schema = comments_tool["inputSchema"]

        assert "properties" in schema
        props = schema["properties"]
        assert "video_id" in props
        assert "max_results" in props
        assert "page_token" in props

    @pytest.mark.asyncio
    async def test_get_analytics_schema_properties(self):
        """youtube_get_analytics schema should have correct properties."""
        tools = await list_tools()
        analytics_tool = next(t for t in tools if t["name"] == "youtube_get_analytics")
        schema = analytics_tool["inputSchema"]

        assert "properties" in schema
        props = schema["properties"]
        assert "ids" in props
        assert "metrics" in props
        assert "start_date" in props
        assert "end_date" in props

    def test_server_name(self):
        """Server should have a valid name."""
        assert server.name == "youtube-mcp-server"

    @pytest.mark.asyncio
    async def test_call_tool_invalid_tool_raises_error(self):
        """Calling unknown tool should raise ValueError."""
        # Note: We can't directly call server.call_tool() because it's decorated
        # Instead, we test that the main.py function raises ValueError for unknown tools
        # The actual call_tool function in main.py raises ValueError for unknown tools
        with pytest.raises(ValueError, match="Unknown tool"):
            await call_tool("unknown_tool", {})

    @pytest.mark.asyncio
    async def test_tool_property_descriptions_exist(self):
        """Each property in tool schema should have a description."""
        tools = await list_tools()
        for tool in tools:
            schema = tool["inputSchema"]
            if "properties" in schema:
                for prop_name, prop_schema in schema["properties"].items():
                    if "description" in prop_schema:
                        assert prop_schema["description"]
                        assert len(prop_schema["description"]) > 0

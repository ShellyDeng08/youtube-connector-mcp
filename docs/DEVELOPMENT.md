# Development Guide

This guide is for contributors who want to develop or extend the YouTube MCP Server.

---

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_tools/test_search.py
```

## Project Structure

```
youtube-mcp-server/  (Repository name)
├── src/
│   ├── main.py              # MCP server entry point
│   ├── youtube_client.py    # YouTube API wrapper
│   ├── config.py            # Configuration
│   └── tools/              # MCP tool implementations
│       ├── search.py
│       ├── video.py
│       ├── channel.py
│       ├── transcript.py
│       ├── playlist.py
│       ├── comments.py
│       └── analytics.py
├── tests/                  # Test suite
├── docs/                   # Documentation
├── pyproject.toml          # Dependencies & config
├── requirements.txt        # Pip requirements
└── README.md
```

## Adding a New Tool

1. Create a new file in `src/tools/`, e.g., `src/tools/new_tool.py`
2. Define your Pydantic args model:
   ```python
   from pydantic import BaseModel

   class NewToolArgs(BaseModel):
       param: str
   ```

3. Implement the async function:
   ```python
   async def new_tool(param: str) -> list[dict]:
       # Your implementation here
       return [{"result": ...}]
   ```

4. Register in `src/main.py`:
   ```python
   from src.tools.new_tool import new_tool, NewToolArgs

   @server.list_tools()
   async def list_tools():
       return [{
           "name": "new_tool",
           "description": "Description of your tool",
           "inputSchema": NewToolArgs.model_json_schema()
       }]
   ```

5. Add tests in `tests/test_tools/test_new_tool.py`

## Building for Distribution

```bash
# Build package
poetry build

# Or using setuptools
python -m build
```

## Publishing to PyPI

```bash
# Upload to PyPI (requires twine)
twine upload dist/*
```

## Related Documentation

- [Technical sharing: Skills, Plugins, and MCP](docs/tech-sharing-skills-plugins-mcp.md)
- [API Key Setup](../README.md#api-key-setup)

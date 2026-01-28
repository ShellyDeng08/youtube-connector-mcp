"""Configuration for YouTube MCP Server."""
import os
from dataclasses import dataclass


@dataclass
class Config:
    """Server configuration."""
    api_key: str
    rate_limit: int = 100


def get_config() -> Config:
    """Load configuration from environment variables."""
    api_key = os.getenv("YOUTUBE_API_KEY", "")
    if not api_key:
        raise ValueError(
            "YOUTUBE_API_KEY environment variable is required. "
            "Set it or add it to your MCP configuration."
        )

    rate_limit = int(os.getenv("YOUTUBE_RATE_LIMIT", "100"))
    return Config(api_key=api_key, rate_limit=rate_limit)

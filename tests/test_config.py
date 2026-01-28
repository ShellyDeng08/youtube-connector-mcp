import os
from src.config import get_config

def test_get_config_with_env():
    os.environ["YOUTUBE_API_KEY"] = "test_key"
    config = get_config()
    assert config.api_key == "test_key"

def test_get_config_defaults():
    # Ensure clean state for YOUTUBE_RATE_LIMIT
    os.environ.pop("YOUTUBE_RATE_LIMIT", None)
    # Set required API key to satisfy config requirements
    os.environ["YOUTUBE_API_KEY"] = "test_key"

    config = get_config()
    assert config.rate_limit == 100

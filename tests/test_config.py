import os
from src.config import get_config

def test_get_config_with_env():
    os.environ["YOUTUBE_API_KEY"] = "test_key"
    config = get_config()
    assert config.api_key == "test_key"

def test_get_config_defaults():
    # Set required API key (use dummy value for testing defaults)
    os.environ["YOUTUBE_API_KEY"] = "test_key_for_defaults"
    # Remove YOUTUBE_RATE_LIMIT to test its default
    os.environ.pop("YOUTUBE_RATE_LIMIT", None)

    config = get_config()
    assert config.api_key == "test_key_for_defaults"
    assert config.rate_limit == 100

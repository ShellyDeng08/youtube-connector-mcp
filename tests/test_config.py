import os
from src.config import get_config

def test_get_config_with_env():
    os.environ["YOUTUBE_API_KEY"] = "test_key"
    config = get_config()
    assert config.api_key == "test_key"

def test_get_config_defaults():
    # Ensure clean state
    for key in ["YOUTUBE_API_KEY", "YOUTUBE_RATE_LIMIT"]:
        os.environ.pop(key, None)

    config = get_config()
    assert config.rate_limit == 100

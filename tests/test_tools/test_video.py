from src.tools.video import youtube_get_video

def test_youtube_get_video_exists():
    assert callable(youtube_get_video)

from src.tools.transcript import youtube_get_transcript

def test_youtube_get_transcript_exists():
    assert callable(youtube_get_transcript)

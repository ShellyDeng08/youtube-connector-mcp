"""Unit tests for youtube_get_analytics tool."""
import pytest
from src.tools.analytics import youtube_get_analytics, GetAnalyticsArgs


@pytest.mark.unit
class TestGetAnalyticsArgs:
    """Test GetAnalyticsArgs Pydantic model."""

    def test_get_analytics_args_defaults(self):
        """GetAnalyticsArgs should use defaults correctly."""
        args = GetAnalyticsArgs(ids="channel==UCabc123")
        assert args.ids == "channel==UCabc123"
        assert args.metrics == ["views", "likes", "comments"]
        assert args.start_date is None
        assert args.end_date is None

    def test_get_analytics_args_custom_values(self):
        """GetAnalyticsArgs should accept custom values."""
        args = GetAnalyticsArgs(
            ids="channel==UCabc123",
            metrics=["views", "estimatedMinutesWatched"],
            start_date="2024-01-01",
            end_date="2024-12-31"
        )
        assert args.ids == "channel==UCabc123"
        assert args.metrics == ["views", "estimatedMinutesWatched"]
        assert args.start_date == "2024-01-01"
        assert args.end_date == "2024-12-31"


@pytest.mark.unit
class TestYouTubeGetAnalytics:
    """Test youtube_get_analytics function."""

    @pytest.mark.asyncio
    async def test_get_analytics_requires_oauth(self):
        """youtube_get_analytics should return AuthRequired error."""
        result = await youtube_get_analytics(
            ids="channel==UCabc123",
            metrics=["views"]
        )

        assert result["data"]["message"]
        assert "OAuth" in result["data"]["message"]
        assert result["error"]["code"] == "AuthRequired"
        assert result["error"]["message"] == "Analytics API requires OAuth scope. Use youtube_get_video/channel for basic stats."
        assert result["pagination"] is None

    @pytest.mark.asyncio
    async def test_get_analytics_suggests_alternative(self):
        """youtube_get_analytics should suggest using youtube_get_video/channel."""
        result = await youtube_get_analytics(ids="channel==UCabc123")

        assert "youtube_get_video" in result["data"]["message"]
        assert "youtube_get_channel" in result["data"]["message"]

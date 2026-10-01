"""Tests for news tab content."""

import pytest
from PySide6.QtWidgets import QLabel

from features.ui.components import NewsArticleCard
from features.ui.news_feed_service import NewsArticle
from features.ui.tabs.news_tab import NewsTabContent, create_news_tab_content


def make_article(title: str = "Article") -> NewsArticle:
    """Build a canned article for tab tests."""
    return NewsArticle(
        title=title,
        url="https://example.com/article",
        source="Test Source",
        published_date=None,
        description="A description",
    )


class FakeFeedService:
    """Stand-in NewsFeedService so tab tests never touch the network."""

    def __init__(self, articles=None, error=None):
        self.articles = articles if articles is not None else []
        self.error = error
        self.calls: list[int] = []

    def fetch_articles(self, limit: int = 10, should_stop=None):
        """Return the canned result or raise the canned error."""
        self.calls.append(limit)
        if self.error:
            raise self.error
        return self.articles


def has_error_label(content: NewsTabContent) -> bool:
    """Check whether the standard fetch-error label is present."""
    return any("Unable to fetch news" in label.text() for label in content.findChildren(QLabel))


class TestNewsTab:
    """Tests for news tab content creation."""

    def test_create_news_tab_content(self, qtbot):
        """Test that news tab content is created successfully."""
        content = create_news_tab_content(feed_service=FakeFeedService())

        qtbot.wait_until(lambda: content._news_worker is None)

        # Verify content is created
        assert content is not None
        assert isinstance(content, NewsTabContent)
        assert content.layout() is not None

    @pytest.mark.usefixtures("qtbot")
    def test_news_tab_content_initialization(self):
        """Test NewsTabContent widget initialization with loading label."""
        content = NewsTabContent(feed_service=FakeFeedService())

        # Verify widget is properly initialized and still loading
        assert content._headlines_layout is not None
        assert content._headlines_loading_label is not None
        assert content.layout() is not None
        assert content.layout().count() > 0

    def test_news_tab_has_static_sources(self):
        """Test that news tab contains static source cards."""
        content = NewsTabContent(feed_service=FakeFeedService())

        # Verify layout exists and has items
        layout = content.layout()
        assert layout is not None
        assert layout.count() > 0

    def test_headlines_render_after_fetch(self, qtbot):
        """Articles arrive by signal and replace the loading label."""
        articles = [make_article("A1"), make_article("A2")]
        content = NewsTabContent(feed_service=FakeFeedService(articles=articles))

        qtbot.wait_until(lambda: content._news_worker is None)

        assert content._headlines_loading_label is None
        cards = content.findChildren(NewsArticleCard)
        assert len(cards) == len(articles)

    def test_error_label_on_empty_articles(self, qtbot):
        """An empty article list shows the standard error label."""
        content = NewsTabContent(feed_service=FakeFeedService(articles=[]))

        qtbot.wait_until(lambda: content._headlines_loading_label is None)

        assert has_error_label(content)

    def test_error_label_on_fetch_failure(self, qtbot):
        """A failing fetch shows the error label instead of crashing."""
        content = NewsTabContent(feed_service=FakeFeedService(error=RuntimeError("offline")))

        qtbot.wait_until(lambda: content._headlines_loading_label is None)

        assert has_error_label(content)

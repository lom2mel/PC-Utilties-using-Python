"""Tests for security tab content."""

from unittest.mock import MagicMock, Mock

from PySide6.QtWidgets import QLabel

from features.ui.components import CompactNewsCard
from features.ui.download_handlers import DownloadHandlers
from features.ui.news_feed_service import NewsArticle
from features.ui.tabs.security_tab import (
    HEADLINE_DISPLAY_COUNT,
    create_security_tab_content,
)


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


def make_download_handlers() -> MagicMock:
    """Build a mocked DownloadHandlers with all security card methods."""
    download_handlers = MagicMock(spec=DownloadHandlers)
    download_handlers.download_avast = Mock()
    download_handlers.open_virustotal = Mock()
    download_handlers.download_ccleaner = Mock()
    download_handlers.download_speccy = Mock()
    download_handlers.download_bitdefender = Mock()
    return download_handlers


def has_error_label(content) -> bool:
    """Check whether the standard fetch-error label is present."""
    return any("Unable to fetch news" in label.text() for label in content.findChildren(QLabel))


class TestSecurityTab:
    """Tests for security tab content creation."""

    def test_create_security_tab_content(self, qtbot):
        """Test that security tab content is created successfully."""
        content = create_security_tab_content(
            make_download_handlers(), feed_service=FakeFeedService()
        )
        qtbot.wait_until(lambda: content._news_worker is None)

        # Verify content is created
        assert content is not None
        assert content.layout() is not None
        assert content.layout().count() > 0

        # Verify content has transparent background
        assert "background: transparent" in content.styleSheet()

    def test_security_tab_has_cards(self, qtbot):
        """Test that security tab contains expected cards."""
        content = create_security_tab_content(
            make_download_handlers(), feed_service=FakeFeedService()
        )
        qtbot.wait_until(lambda: content._news_worker is None)
        layout = content.layout()

        # Find all child widgets
        cards = []
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                # Recursively find ModernCard widgets
                cards.extend(widget.findChildren(type(widget)))

        # Verify we have the security tool cards
        assert len(cards) > 0

    def test_loading_label_shown_until_fetch_completes(self, qtbot):
        """The loading label is present at construction and removed after."""
        content = create_security_tab_content(
            make_download_handlers(), feed_service=FakeFeedService()
        )

        assert content._news_loading_label is not None

        qtbot.wait_until(lambda: content._news_worker is None)

        assert content._news_loading_label is None

    def test_headlines_capped_at_display_count(self, qtbot):
        """Only HEADLINE_DISPLAY_COUNT compact cards are rendered."""
        articles = [make_article(f"A{i}") for i in range(HEADLINE_DISPLAY_COUNT + 2)]
        content = create_security_tab_content(
            make_download_handlers(),
            feed_service=FakeFeedService(articles=articles),
        )

        qtbot.wait_until(lambda: content._news_worker is None)

        cards = content.findChildren(CompactNewsCard)
        assert len(cards) == HEADLINE_DISPLAY_COUNT

    def test_error_label_on_empty_articles(self, qtbot):
        """An empty article list shows the standard error label."""
        content = create_security_tab_content(
            make_download_handlers(), feed_service=FakeFeedService(articles=[])
        )

        qtbot.wait_until(lambda: content._news_loading_label is None)

        assert has_error_label(content)

    def test_error_label_on_fetch_failure(self, qtbot):
        """A failing fetch shows the error label instead of crashing."""
        content = create_security_tab_content(
            make_download_handlers(),
            feed_service=FakeFeedService(error=RuntimeError("offline")),
        )

        qtbot.wait_until(lambda: content._news_loading_label is None)

        assert has_error_label(content)

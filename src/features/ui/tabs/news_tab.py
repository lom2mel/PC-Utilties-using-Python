"""Cybersecurity news tab content for PC Utilities Manager.

This module provides the cybersecurity news tab with static sources
and live RSS feed headlines.
"""

import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from features.ui.components import ModernCard, NewsArticleCard, SectionHeader
from features.ui.design_system import COLORS, SPACING, TYPOGRAPHY
from features.ui.news_feed_service import NewsFeedService
from features.ui.news_feed_worker import NewsFeedWorker
from features.ui.security_utils import validate_and_open_url

logger = logging.getLogger(__name__)

# Configuration constants
DEFAULT_ARTICLE_LIMIT = 15  # Number of articles to fetch per source


class NewsTabContent(QWidget):
    """Cybersecurity news tab with static sources and live headlines.

    This widget provides both static curated news sources and dynamic
    RSS feed aggregation. Headlines are loaded asynchronously to
    prevent UI freezing.
    """

    def __init__(self, feed_service: NewsFeedService | None = None, parent=None):
        """Initialize the news tab content.

        Args:
            feed_service: Optional news feed service (injected in tests)
            parent: Optional parent widget
        """
        super().__init__(parent)
        self._feed_service = feed_service or NewsFeedService()
        self._news_worker: NewsFeedWorker | None = None
        self._headlines_layout = None
        self._headlines_loading_label = None
        self._init_ui()

        # Fetch headlines on a background thread; the GUI stays responsive
        self._start_headlines_fetch()

    def _init_ui(self) -> None:
        """Initialize the news tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING.LG)

        # Section header
        header = SectionHeader(
            "📰 Cyber Security News",
            "Stay informed with the latest cybersecurity headlines and resources",
        )
        layout.addWidget(header)

        # Static sources section label
        static_label = QLabel("Trusted News Sources")
        static_label.setFont(
            QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_SECTION_HEADER, QFont.Bold)
        )
        static_label.setStyleSheet(f"color: {COLORS.TEXT_PRIMARY};")
        layout.addWidget(static_label)

        # Static sources grid
        static_grid = QGridLayout()
        static_grid.setSpacing(SPACING.MD)

        for idx, source in enumerate(NewsFeedService.STATIC_SOURCES):
            card = ModernCard(
                source["title"], source["description"], source["icon"], COLORS.GRADIENT_START
            )
            # Store URL in closure for secure click handler
            url = source["url"]
            card.mousePressEvent = lambda e, u=url: validate_and_open_url(u)
            row, col = divmod(idx, 3)
            static_grid.addWidget(card, row, col)

        layout.addLayout(static_grid)

        # Live headlines section label
        headlines_label = QLabel("Latest Headlines")
        headlines_label.setFont(
            QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_SECTION_HEADER, QFont.Bold)
        )
        headlines_label.setStyleSheet(f"color: {COLORS.TEXT_PRIMARY}; margin-top: {SPACING.LG}px;")
        layout.addWidget(headlines_label)

        # Scrollable headlines list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(f"border: none; background-color: {COLORS.BACKGROUND_PRIMARY};")

        headlines_widget = QWidget()
        headlines_layout = QVBoxLayout(headlines_widget)
        headlines_layout.setSpacing(SPACING.SM)
        headlines_layout.setContentsMargins(0, 0, 0, SPACING.LG)

        # Add loading label
        self._headlines_loading_label = QLabel("Loading latest headlines...")
        self._headlines_loading_label.setFont(
            QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_BODY_SMALL)
        )
        self._headlines_loading_label.setStyleSheet(f"color: {COLORS.TEXT_SECONDARY};")
        self._headlines_loading_label.setAlignment(Qt.AlignCenter)
        headlines_layout.addWidget(self._headlines_loading_label)

        scroll.setWidget(headlines_widget)
        layout.addWidget(scroll, 1)  # Give stretch factor

        # Store reference to layout for deferred loading
        self._headlines_layout = headlines_layout

    def _start_headlines_fetch(self) -> None:
        """Start the background RSS fetch and wire its result signals.

        Connections are made before ``start()`` so fast results cannot be
        missed. The worker keeps itself referenced until its thread exits
        (see ``NewsFeedWorker._live``); this tab only mirrors the running
        state for tests and clears it on the built-in ``finished`` signal.
        """
        worker = NewsFeedWorker(self._feed_service, DEFAULT_ARTICLE_LIMIT)
        worker.articles_ready.connect(self._on_articles_ready)
        worker.fetch_failed.connect(self._on_fetch_failed)
        worker.finished.connect(self._on_worker_finished)
        self._news_worker = worker
        worker.start()

    def _on_worker_finished(self) -> None:
        """Release the worker reference once its thread has exited."""
        self._news_worker = None

    def _on_articles_ready(self, articles: list) -> None:
        """Render fetched headlines in the scroll area (main thread slot).

        Args:
            articles: Fetched NewsArticle objects (possibly empty)
        """
        self._remove_headlines_loading_label()

        if not hasattr(self, "_headlines_layout"):
            return

        if not articles:
            self._add_news_error_label()
            self._headlines_layout.addStretch()
            return

        for article in articles:
            card = NewsArticleCard(article)
            self._headlines_layout.addWidget(card)

        self._headlines_layout.addStretch()

    def _on_fetch_failed(self, message: str) -> None:
        """Show the error label when the background fetch fails.

        Args:
            message: Error description from the worker
        """
        logger.warning(f"Headlines fetch failed: {message}")
        self._remove_headlines_loading_label()
        self._add_news_error_label()

    def _remove_headlines_loading_label(self) -> None:
        """Remove the loading label from the headlines list, if present."""
        if self._headlines_loading_label is not None:
            self._headlines_loading_label.setParent(None)
            self._headlines_loading_label = None

    def _add_news_error_label(self) -> None:
        """Add the standard 'unable to fetch' label to the headlines list."""
        no_news = QLabel("Unable to fetch news. Please check your internet connection.")
        no_news.setFont(QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_BODY_NORMAL))
        no_news.setStyleSheet(f"color: {COLORS.TEXT_SECONDARY}; padding: {SPACING.LG}px;")
        no_news.setAlignment(Qt.AlignCenter)
        self._headlines_layout.addWidget(no_news)


def create_news_tab_content(feed_service: NewsFeedService | None = None) -> QWidget:
    """Create cybersecurity news tab content with static sources and live headlines.

    Args:
        feed_service: Optional news feed service (injected in tests)

    Returns:
        Widget with news sources and live RSS feed headlines
    """
    return NewsTabContent(feed_service=feed_service)

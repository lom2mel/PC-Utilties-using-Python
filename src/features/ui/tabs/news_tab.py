"""Cybersecurity news tab content for PC Utilities Manager.

This module provides the cybersecurity news tab with static sources
and live RSS feed headlines.
"""

import webbrowser
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QScrollArea,
    QFrame,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from features.ui.components import SectionHeader, ModernCard, NewsArticleCard
from features.ui.design_system import COLORS, TYPOGRAPHY, SPACING
from features.ui.news_feed_service import NewsFeedService


class NewsTabContent(QWidget):
    """Cybersecurity news tab with static sources and live headlines.

    This widget provides both static curated news sources and dynamic
    RSS feed aggregation. Headlines are loaded asynchronously to
    prevent UI freezing.
    """

    def __init__(self, parent=None):
        """Initialize the news tab content.

        Args:
            parent: Optional parent widget
        """
        super().__init__(parent)
        self._headlines_layout = None
        self._headlines_loading_label = None
        self._init_ui()

        # Defer RSS fetching to avoid UI freeze
        QTimer.singleShot(100, self._populate_headlines)

    def _init_ui(self) -> None:
        """Initialize the news tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING.LG)

        # Section header
        header = SectionHeader(
            "📰 Cyber Security News",
            "Stay informed with the latest cybersecurity headlines and resources"
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
                source["title"],
                source["description"],
                source["icon"],
                COLORS.GRADIENT_START
            )
            # Store URL in closure for click handler
            url = source["url"]
            card.mousePressEvent = lambda e, u=url: webbrowser.open(u)
            row, col = divmod(idx, 3)
            static_grid.addWidget(card, row, col)

        layout.addLayout(static_grid)

        # Live headlines section label
        headlines_label = QLabel("Latest Headlines")
        headlines_label.setFont(
            QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_SECTION_HEADER, QFont.Bold)
        )
        headlines_label.setStyleSheet(
            f"color: {COLORS.TEXT_PRIMARY}; margin-top: {SPACING.LG}px;"
        )
        layout.addWidget(headlines_label)

        # Scrollable headlines list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(
            f"border: none; background-color: {COLORS.BACKGROUND_PRIMARY};"
        )

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

    def _populate_headlines(self) -> None:
        """Populate headlines layout with fetched articles (called via QTimer)."""
        # Remove loading label
        if (
            hasattr(self, "_headlines_loading_label")
            and self._headlines_loading_label
        ):
            self._headlines_loading_label.setParent(None)
            self._headlines_loading_label = None

        if not hasattr(self, "_headlines_layout"):
            return

        service = NewsFeedService()
        articles = service.fetch_articles(limit=15)

        if not articles:
            no_news = QLabel(
                "Unable to fetch news. Please check your internet connection."
            )
            no_news.setFont(
                QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_BODY_NORMAL)
            )
            no_news.setStyleSheet(
                f"color: {COLORS.TEXT_SECONDARY}; padding: {SPACING.LG}px;"
            )
            no_news.setAlignment(Qt.AlignCenter)
            self._headlines_layout.addWidget(no_news)
            self._headlines_layout.addStretch()
            return

        for article in articles:
            card = NewsArticleCard(article)
            self._headlines_layout.addWidget(card)

        self._headlines_layout.addStretch()


def create_news_tab_content() -> QWidget:
    """Create cybersecurity news tab content with static sources and live headlines.

    Returns:
        Widget with news sources and live RSS feed headlines
    """
    return NewsTabContent()

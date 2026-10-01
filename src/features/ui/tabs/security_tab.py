"""Security tools tab content for PC Utilities Manager.

This module provides the security & maintenance tools tab with a cybersecurity
news headlines section and cards for downloading antivirus and security utilities.
"""

import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from features.ui.components import CompactNewsCard, ModernCard, SectionHeader
from features.ui.design_system import COLORS, SPACING, TYPOGRAPHY
from features.ui.download_handlers import DownloadHandlers
from features.ui.news_feed_service import NewsFeedService
from features.ui.news_feed_worker import NewsFeedWorker

logger = logging.getLogger(__name__)

# Configuration constants
DEFAULT_ARTICLE_LIMIT = 10  # Number of articles to fetch per source
HEADLINE_DISPLAY_COUNT = 3  # Number of headlines to display in compact view


class SecurityTabContent(QWidget):
    """Security & Maintenance tools tab with news headlines and tool cards.

    This widget provides a compact cybersecurity news headlines section at the
    top, followed by a grid of security tool cards. Headlines are loaded
    asynchronously to prevent UI freezing.

    Attributes:
        download_handlers: Handler for download operations
    """

    def __init__(
        self,
        download_handlers: DownloadHandlers,
        feed_service: NewsFeedService | None = None,
        parent=None,
    ):
        """Initialize the security tab content.

        Args:
            download_handlers: Handler for download operations
            feed_service: Optional news feed service (injected in tests)
            parent: Optional parent widget
        """
        super().__init__(parent)
        self.download_handlers = download_handlers
        self._feed_service = feed_service or NewsFeedService()
        self._news_worker: NewsFeedWorker | None = None
        self._news_layout = None
        self._news_loading_label = None
        self._init_ui()

        # Fetch headlines on a background thread; the GUI stays responsive
        self._start_headlines_fetch()

    def _init_ui(self) -> None:
        """Initialize the security tab UI."""
        layout = QVBoxLayout()
        layout.setSpacing(SPACING.LG)
        layout.addWidget(self._create_header())
        layout.addWidget(self._create_news_section())
        layout.addLayout(self._create_cards_section())
        layout.addStretch()
        self.setLayout(layout)

    def _create_header(self) -> SectionHeader:
        """Create the section header.

        Returns:
            Configured section header widget
        """
        return SectionHeader(
            "🔒 Security & Maintenance Tools",
            "Download and use essential security utilities to keep your PC safe",
        )

    def _create_news_section(self) -> QFrame:
        """Create the news headlines section with async loading support.

        Returns:
            Configured news container frame
        """
        # News container for async loading
        news_container = QFrame()
        news_container.setStyleSheet("background-color: transparent;")
        news_layout = QVBoxLayout(news_container)
        news_layout.setSpacing(SPACING.SM)
        news_layout.setContentsMargins(0, 0, 0, 0)

        # Add loading label
        self._news_loading_label = QLabel("Loading latest headlines...")
        self._news_loading_label.setFont(QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_BODY_SMALL))
        self._news_loading_label.setStyleSheet(f"color: {COLORS.TEXT_SECONDARY};")
        self._news_loading_label.setAlignment(Qt.AlignCenter)
        news_layout.addWidget(self._news_loading_label)

        # Store reference to layout for deferred loading
        self._news_layout = news_layout

        # Add section label above container
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        news_label = QLabel("Latest Cybersecurity Headlines")
        news_label.setFont(
            QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_SECTION_HEADER, QFont.Bold)
        )
        news_label.setStyleSheet(f"color: {COLORS.TEXT_PRIMARY};")
        section_layout.addWidget(news_label)
        section_layout.addWidget(news_container)

        return section_widget

    def _create_cards_section(self) -> QGridLayout:
        """Create the security tool cards grid layout.

        Returns:
            Configured grid layout with security tool cards
        """
        cards_layout = QGridLayout()
        cards_layout.setSpacing(SPACING.MD)

        # Create and add security tool cards
        cards_layout.addWidget(self._create_avast_card(), 0, 0)
        cards_layout.addWidget(self._create_virustotal_card(), 0, 1)
        cards_layout.addWidget(self._create_ccleaner_card(), 0, 2)
        cards_layout.addWidget(self._create_speccy_card(), 1, 0)
        cards_layout.addWidget(self._create_bitdefender_card(), 1, 1)

        return cards_layout

    def _create_avast_card(self) -> ModernCard:
        """Create Avast Antivirus download card.

        Returns:
            Configured Avast card
        """
        card = ModernCard(
            "Avast Antivirus", "Download free antivirus protection for your PC", "🛡️", "#FF6600"
        )
        card.mousePressEvent = lambda e: self.download_handlers.download_avast()
        return card

    def _create_virustotal_card(self) -> ModernCard:
        """Create VirusTotal scanner card.

        Returns:
            Configured VirusTotal card
        """
        card = ModernCard(
            "VirusTotal Scanner", "Scan files for viruses and malware online", "🔍", "#394EFF"
        )
        card.mousePressEvent = lambda e: self.download_handlers.open_virustotal()
        return card

    def _create_ccleaner_card(self) -> ModernCard:
        """Create CCleaner download card.

        Returns:
            Configured CCleaner card
        """
        card = ModernCard("CCleaner", "Clean and optimize your PC performance", "🧹", "#0066CC")
        card.mousePressEvent = lambda e: self.download_handlers.download_ccleaner()
        return card

    def _create_speccy_card(self) -> ModernCard:
        """Create Speccy system information card.

        Returns:
            Configured Speccy card
        """
        card = ModernCard(
            "Speccy", "View detailed system information and specifications", "💻", "#00A4EF"
        )
        card.mousePressEvent = lambda e: self.download_handlers.download_speccy()
        return card

    def _create_bitdefender_card(self) -> ModernCard:
        """Create Bitdefender Antivirus download card.

        Returns:
            Configured Bitdefender card
        """
        card = ModernCard(
            "Bitdefender Antivirus",
            "Download free antivirus protection for your PC",
            "🦠",
            "#ED1C24",
        )
        card.mousePressEvent = lambda e: self.download_handlers.download_bitdefender()
        return card

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
        """Render fetched headlines in the news section (main thread slot).

        Args:
            articles: Fetched NewsArticle objects (possibly empty)
        """
        self._remove_news_loading_label()

        if not articles:
            self._add_news_error_label()
            return

        # Show only limited articles for compact display
        for article in articles[:HEADLINE_DISPLAY_COUNT]:
            card = CompactNewsCard(article)
            self._news_layout.addWidget(card)

    def _on_fetch_failed(self, message: str) -> None:
        """Show the error label when the background fetch fails.

        Args:
            message: Error description from the worker
        """
        logger.warning(f"Headlines fetch failed: {message}")
        self._remove_news_loading_label()
        self._add_news_error_label()

    def _remove_news_loading_label(self) -> None:
        """Remove the loading label from the news section, if present."""
        if self._news_loading_label is not None:
            self._news_loading_label.setParent(None)
            self._news_loading_label = None

    def _add_news_error_label(self) -> None:
        """Add the standard 'unable to fetch' label to the news section."""
        no_news = QLabel("Unable to fetch news. Please check your internet connection.")
        no_news.setFont(QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_BODY_SMALL))
        no_news.setStyleSheet(f"color: {COLORS.TEXT_SECONDARY}; padding: {SPACING.SM}px;")
        no_news.setAlignment(Qt.AlignCenter)
        self._news_layout.addWidget(no_news)


def create_security_tab_content(
    download_handlers: DownloadHandlers,
    feed_service: NewsFeedService | None = None,
) -> QWidget:
    """Create security tools tab content with news headlines and cards.

    Args:
        download_handlers: Handler for download operations
        feed_service: Optional news feed service (injected in tests)

    Returns:
        Widget with news headlines and security tool cards
    """
    return SecurityTabContent(download_handlers, feed_service=feed_service)

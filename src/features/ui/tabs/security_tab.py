"""Security tools tab content for PC Utilities Manager.

This module provides the security & maintenance tools tab with a cybersecurity
news headlines section and cards for downloading antivirus and security utilities.
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QGridLayout,
    QVBoxLayout,
    QWidget,
)

from features.ui.components import ModernCard, CompactNewsCard, SectionHeader
from features.ui.design_system import COLORS, SPACING, TYPOGRAPHY
from features.ui.download_handlers import DownloadHandlers
from features.ui.news_feed_service import NewsFeedService


class SecurityTabContent(QWidget):
    """Security & Maintenance tools tab with news headlines and tool cards.

    This widget provides a compact cybersecurity news headlines section at the
    top, followed by a grid of security tool cards. Headlines are loaded
    asynchronously to prevent UI freezing.

    Attributes:
        download_handlers: Handler for download operations
    """

    def __init__(self, download_handlers: DownloadHandlers, parent=None):
        """Initialize the security tab content.

        Args:
            download_handlers: Handler for download operations
            parent: Optional parent widget
        """
        super().__init__(parent)
        self.download_handlers = download_handlers
        self._news_layout = None
        self._news_loading_label = None
        self._init_ui()

        # Defer RSS fetching to avoid UI freeze
        QTimer.singleShot(100, self._populate_headlines)

    def _init_ui(self) -> None:
        """Initialize the security tab UI."""
        layout = QVBoxLayout()
        layout.setSpacing(SPACING.LG)

        # Section header
        header = SectionHeader(
            "🔒 Security & Maintenance Tools",
            "Download and use essential security utilities to keep your PC safe"
        )
        layout.addWidget(header)

        # News headlines section
        news_label = QLabel("Latest Cybersecurity Headlines")
        news_label.setFont(
            QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_SECTION_HEADER, QFont.Bold)
        )
        news_label.setStyleSheet(f"color: {COLORS.TEXT_PRIMARY};")
        layout.addWidget(news_label)

        # News container for async loading
        news_container = QFrame()
        news_container.setStyleSheet(f"background-color: transparent;")
        news_layout = QVBoxLayout(news_container)
        news_layout.setSpacing(SPACING.SM)
        news_layout.setContentsMargins(0, 0, 0, 0)

        # Add loading label
        self._news_loading_label = QLabel("Loading latest headlines...")
        self._news_loading_label.setFont(
            QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_BODY_SMALL)
        )
        self._news_loading_label.setStyleSheet(f"color: {COLORS.TEXT_SECONDARY};")
        self._news_loading_label.setAlignment(Qt.AlignCenter)
        news_layout.addWidget(self._news_loading_label)

        layout.addWidget(news_container)

        # Store reference to layout for deferred loading
        self._news_layout = news_layout

        # Security tool cards section
        cards_layout = QGridLayout()
        cards_layout.setSpacing(SPACING.MD)

        # Avast card
        avast_card = ModernCard(
            "Avast Antivirus",
            "Download free antivirus protection for your PC",
            "🛡️",
            "#FF6600"
        )
        avast_card.mousePressEvent = lambda e: self.download_handlers.download_avast()
        cards_layout.addWidget(avast_card, 0, 0)

        # VirusTotal card
        virustotal_card = ModernCard(
            "VirusTotal Scanner",
            "Scan files for viruses and malware online",
            "🔍",
            "#394EFF"
        )
        virustotal_card.mousePressEvent = lambda e: self.download_handlers.open_virustotal()
        cards_layout.addWidget(virustotal_card, 0, 1)

        # CCleaner card
        ccleaner_card = ModernCard(
            "CCleaner",
            "Clean and optimize your PC performance",
            "🧹",
            "#0066CC"
        )
        ccleaner_card.mousePressEvent = lambda e: self.download_handlers.download_ccleaner()
        cards_layout.addWidget(ccleaner_card, 0, 2)

        # Speccy card
        speccy_card = ModernCard(
            "Speccy",
            "View detailed system information and specifications",
            "💻",
            "#00A4EF"
        )
        speccy_card.mousePressEvent = lambda e: self.download_handlers.download_speccy()
        cards_layout.addWidget(speccy_card, 1, 0)

        # Bitdefender card
        bitdefender_card = ModernCard(
            "Bitdefender Antivirus",
            "Download free antivirus protection for your PC",
            "🦠",
            "#ED1C24"
        )
        bitdefender_card.mousePressEvent = lambda e: self.download_handlers.download_bitdefender()
        cards_layout.addWidget(bitdefender_card, 1, 1)

        layout.addLayout(cards_layout)
        layout.addStretch()

        self.setLayout(layout)

    def _populate_headlines(self) -> None:
        """Populate headlines layout with fetched articles (called via QTimer)."""
        # Remove loading label
        if (
            hasattr(self, "_news_loading_label")
            and self._news_loading_label
        ):
            self._news_loading_label.setParent(None)
            self._news_loading_label = None

        if not hasattr(self, "_news_layout"):
            return

        service = NewsFeedService()
        articles = service.fetch_articles(limit=10)

        if not articles:
            no_news = QLabel(
                "Unable to fetch news. Please check your internet connection."
            )
            no_news.setFont(
                QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_BODY_SMALL)
            )
            no_news.setStyleSheet(
                f"color: {COLORS.TEXT_SECONDARY}; padding: {SPACING.SM}px;"
            )
            no_news.setAlignment(Qt.AlignCenter)
            self._news_layout.addWidget(no_news)
            return

        # Show only 3 articles for compact display
        for article in articles[:3]:
            card = CompactNewsCard(article)
            self._news_layout.addWidget(card)


def create_security_tab_content(download_handlers: DownloadHandlers) -> QWidget:
    """Create security tools tab content with news headlines and cards.

    Args:
        download_handlers: Handler for download operations

    Returns:
        Widget with news headlines and security tool cards
    """
    return SecurityTabContent(download_handlers)

"""Antivirus Sales and Discounts tab content for PC Utilities Manager.

This module provides the antivirus deals tab with cards linking to popular
antivirus vendor websites with their current sales, promotions, and discounts.
"""

import webbrowser
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QGridLayout,
    QVBoxLayout,
    QWidget,
)

from features.ui.components import ModernCard, SectionHeader
from features.ui.design_system import COLORS, SPACING


class AntivirusDealsTabContent(QWidget):
    """Antivirus Sales and Discounts tab with vendor deal cards.

    This widget provides a grid of cards for popular antivirus vendors.
    Clicking a card opens the vendor's deals/sales page in a web browser.

    Attributes:
        None: This tab does not require any handlers
    """

    # Vendor deals URLs
    NORTON_URL = "https://us.norton.com/discounts"
    MCAFEE_URL = "https://www.mcafee.com/consumer/en-us/store/index.html"
    BITDEFENDER_URL = "https://www.bitdefender.com/site/View/promotions.html"
    KASPERSKY_URL = "https://www.kaspersky.com/promotions-discounts"
    AVAST_URL = "https://www.avast.com/lp-sales-us"
    AVIRA_URL = "https://www.avira.com/en/promotions"
    MALWAREBYTES_URL = "https://www.malwarebytes.com/pricing/"
    TREND_MICRO_URL = "https://www.trendmicro.com/en_us/promo.html"

    def __init__(self, parent=None):
        """Initialize the antivirus deals tab content.

        Args:
            parent: Optional parent widget
        """
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the antivirus deals tab UI."""
        layout = QVBoxLayout()
        layout.setSpacing(SPACING.LG)

        # Section header
        header = SectionHeader(
            "🏷️ Antivirus Sales and Discounts",
            "Click any vendor below to view their current promotions, sales, and discounted offers"
        )
        layout.addWidget(header)

        # Create grid of vendor cards
        cards_layout = QGridLayout()
        cards_layout.setSpacing(SPACING.MD)

        # Row 0
        # Norton card - Yellow/Gold brand color
        norton_card = ModernCard(
            "Norton",
            "View current Norton discounts and promotional offers",
            "🛡️",
            "#FFCC00"
        )
        norton_card.mousePressEvent = lambda e: self._open_url(self.NORTON_URL)
        cards_layout.addWidget(norton_card, 0, 0)

        # McAfee card - Red brand color
        mcafee_card = ModernCard(
            "McAfee",
            "Explore McAfee sales and special pricing offers",
            "🔐",
            "#C01927"
        )
        mcafee_card.mousePressEvent = lambda e: self._open_url(self.MCAFEE_URL)
        cards_layout.addWidget(mcafee_card, 0, 1)

        # Bitdefender card - Red brand color
        bitdefender_card = ModernCard(
            "Bitdefender",
            "Check out Bitdefender promotions and discounts",
            "🦠",
            "#ED1C24"
        )
        bitdefender_card.mousePressEvent = lambda e: self._open_url(self.BITDEFENDER_URL)
        cards_layout.addWidget(bitdefender_card, 0, 2)

        # Row 1
        # Kaspersky card - Green brand color
        kaspersky_card = ModernCard(
            "Kaspersky",
            "View Kaspersky promotional deals and offers",
            "🌿",
            "#00A98F"
        )
        kaspersky_card.mousePressEvent = lambda e: self._open_url(self.KASPERSKY_URL)
        cards_layout.addWidget(kaspersky_card, 1, 0)

        # Avast card - Orange brand color
        avast_card = ModernCard(
            "Avast",
            "See Avast sales and discounted pricing",
            "🎯",
            "#FF6600"
        )
        avast_card.mousePressEvent = lambda e: self._open_url(self.AVAST_URL)
        cards_layout.addWidget(avast_card, 1, 1)

        # Avira card - Red brand color
        avira_card = ModernCard(
            "Avira",
            "Discover Avira promotions and special offers",
            "⭐",
            "#D32027"
        )
        avira_card.mousePressEvent = lambda e: self._open_url(self.AVIRA_URL)
        cards_layout.addWidget(avira_card, 1, 2)

        # Row 2
        # Malwarebytes card - Blue brand color
        malwarebytes_card = ModernCard(
            "Malwarebytes",
            "Browse Malwarebytes pricing and deals",
            "🔍",
            "#1E449D"
        )
        malwarebytes_card.mousePressEvent = lambda e: self._open_url(self.MALWAREBYTES_URL)
        cards_layout.addWidget(malwarebytes_card, 2, 0)

        # Trend Micro card - Purple brand color
        trend_micro_card = ModernCard(
            "Trend Micro",
            "View Trend Micro promotional offers",
            "🌐",
            "#6A1B9A"
        )
        trend_micro_card.mousePressEvent = lambda e: self._open_url(self.TREND_MICRO_URL)
        cards_layout.addWidget(trend_micro_card, 2, 1)

        layout.addLayout(cards_layout)
        layout.addStretch()

        self.setLayout(layout)

    def _open_url(self, url: str) -> None:
        """Open URL in the default web browser.

        Args:
            url: The URL to open
        """
        try:
            webbrowser.open(url)
        except Exception:
            # Silently fail on browser open error
            pass


def create_antivirus_deals_tab_content(parent=None) -> QWidget:
    """Create antivirus sales and discounts tab content.

    Args:
        parent: Optional parent widget

    Returns:
        Widget with antivirus vendor deal cards
    """
    return AntivirusDealsTabContent(parent)

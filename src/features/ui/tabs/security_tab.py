"""Security tools tab content for PC Utilities Manager.

This module provides the security & maintenance tools tab with cards
for downloading antivirus and security utilities.
"""

from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout
from PySide6.QtCore import Qt

from features.ui.components import ModernCard, SectionHeader
from features.ui.download_handlers import DownloadHandlers


def create_security_tab_content(download_handlers: DownloadHandlers) -> QWidget:
    """Create security tools tab content with cards.

    Args:
        download_handlers: Handler for download operations

    Returns:
        Widget with security tool cards for the security tab
    """
    from PySide6.QtWidgets import QWidget

    content = QWidget()
    content.setStyleSheet("background: transparent;")
    layout = QVBoxLayout()
    layout.setSpacing(20)

    # Section header
    header = SectionHeader(
        "🔒 Security & Maintenance Tools",
        "Download and use essential security utilities to keep your PC safe"
    )
    layout.addWidget(header)

    # Cards grid
    cards_layout = QGridLayout()
    cards_layout.setSpacing(20)

    # Avast card
    avast_card = ModernCard(
        "Avast Antivirus",
        "Download free antivirus protection for your PC",
        "🛡️",
        "#FF6600"
    )
    avast_card.mousePressEvent = lambda e: download_handlers.download_avast()
    cards_layout.addWidget(avast_card, 0, 0)

    # VirusTotal card
    virustotal_card = ModernCard(
        "VirusTotal Scanner",
        "Scan files for viruses and malware online",
        "🔍",
        "#394EFF"
    )
    virustotal_card.mousePressEvent = lambda e: download_handlers.open_virustotal()
    cards_layout.addWidget(virustotal_card, 0, 1)

    # CCleaner card
    ccleaner_card = ModernCard(
        "CCleaner",
        "Clean and optimize your PC performance",
        "🧹",
        "#0066CC"
    )
    ccleaner_card.mousePressEvent = lambda e: download_handlers.download_ccleaner()
    cards_layout.addWidget(ccleaner_card, 0, 2)

    # Speccy card
    speccy_card = ModernCard(
        "Speccy",
        "View detailed system information and specifications",
        "💻",
        "#00A4EF"
    )
    speccy_card.mousePressEvent = lambda e: download_handlers.download_speccy()
    cards_layout.addWidget(speccy_card, 1, 0)

    # Bitdefender card
    bitdefender_card = ModernCard(
        "Bitdefender Antivirus",
        "Download free antivirus protection for your PC",
        "🦠",
        "#ED1C24"
    )
    bitdefender_card.mousePressEvent = lambda e: download_handlers.download_bitdefender()
    cards_layout.addWidget(bitdefender_card, 1, 1)

    layout.addLayout(cards_layout)
    layout.addStretch()
    content.setLayout(layout)
    return content

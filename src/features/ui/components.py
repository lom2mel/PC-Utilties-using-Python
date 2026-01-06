"""UI components for PC Utilities Manager.

This module contains reusable UI widgets including cards and section headers.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class ModernCard(QFrame):
    """Modern card widget with hover effects.

    A card component that displays an icon, title, and description with
    interactive hover states for better user experience.

    Attributes:
        title: The card title text
        description: The card description text
        icon_text: Emoji or icon to display
        color: Accent color for the icon and hover effect
    """

    def __init__(self, title: str, description: str, icon_text: str, color: str):
        """Initialize a ModernCard widget.

        Args:
            title: The title text to display
            description: Descriptive text for the card
            icon_text: Emoji or icon character
            color: Hex color code for accent (e.g., "#FF6600")
        """
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            ModernCard {{
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                padding: 20px;
            }}
            ModernCard:hover {{
                border: 2px solid {color};
                background-color: #FAFAFA;
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)
        self.setup_ui(title, description, icon_text, color)

    def setup_ui(self, title: str, description: str, icon_text: str, color: str) -> None:
        """Setup the card UI layout.

        Args:
            title: The title text to display
            description: Descriptive text for the card
            icon_text: Emoji or icon character
            color: Hex color code for accent
        """
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Icon area
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                border-radius: 30px;
                font-size: 28px;
                font-weight: bold;
                padding: 15px;
            }}
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedSize(60, 60)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title_label.setStyleSheet("color: #1F1F1F;")
        title_label.setWordWrap(True)

        # Description
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 9))
        desc_label.setStyleSheet("color: #666666;")
        desc_label.setWordWrap(True)

        layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()

        self.setLayout(layout)


class SectionHeader(QWidget):
    """Section header widget with title and optional description.

    A reusable header component for organizing UI sections with clear
    visual hierarchy.

    Attributes:
        title: The section title
        description: Optional descriptive text
    """

    def __init__(self, title: str, description: str = ""):
        """Initialize a SectionHeader widget.

        Args:
            title: The section title text
            description: Optional description subtitle
        """
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setStyleSheet("color: #1F1F1F;")

        layout.addWidget(title_label)

        if description:
            desc_label = QLabel(description)
            desc_label.setFont(QFont("Segoe UI", 9))
            desc_label.setStyleSheet("color: #666666;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        self.setLayout(layout)

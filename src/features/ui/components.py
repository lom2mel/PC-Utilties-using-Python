"""Frozen UI Components for PC Utilities Manager.

This module provides reusable UI widgets that adhere to the frozen design system.
All components use immutable design tokens to ensure consistency.

IMPORTANT: These components are part of the frozen UI/UX v2.0 standard.
Modifications must maintain design system integrity.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from features.ui.design_system import (
    COLORS,
    TYPOGRAPHY,
    SPACING,
    BORDERS,
    ICONS,
    StyleSheetTemplates,
)


class ModernCard(QFrame):
    """Modern card widget with frozen design tokens.

    A card component that displays an icon, title, and description with
    interactive hover states. All styling uses the frozen design system.

    The card's appearance is immutable and follows the v2.0 design standard.

    Attributes:
        title: The card title text
        description: The card description text
        icon_text: Emoji or icon to display
        color: Accent color for the icon and hover effect
    """

    def __init__(self, title: str, description: str, icon_text: str, color: str):
        """Initialize a ModernCard widget with frozen styling.

        Args:
            title: The title text to display
            description: Descriptive text for the card
            icon_text: Emoji or icon character
            color: Hex color code for accent (e.g., "#FF6600")

        Note:
            All styling uses frozen design tokens from the design system.
        """
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)

        # Apply frozen design system stylesheet
        self.setStyleSheet(StyleSheetTemplates.card_widget(color))
        self.setCursor(Qt.PointingHandCursor)
        self.setup_ui(title, description, icon_text, color)

    def setup_ui(self, title: str, description: str, icon_text: str, color: str) -> None:
        """Setup the card UI layout using frozen spacing tokens.

        Args:
            title: The title text to display
            description: Descriptive text for the card
            icon_text: Emoji or icon character
            color: Hex color code for accent
        """
        layout = QVBoxLayout()
        layout.setSpacing(SPACING.MD)

        # Icon area with frozen design tokens
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet(StyleSheetTemplates.card_icon_widget(color))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedSize(SPACING.CARD_ICON_SIZE, SPACING.CARD_ICON_SIZE)

        # Title with frozen typography
        title_label = QLabel(title)
        title_label.setFont(QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_CARD_TITLE, QFont.Bold))
        title_label.setStyleSheet(f"color: {COLORS.TEXT_PRIMARY};")
        title_label.setWordWrap(True)

        # Description with frozen typography
        desc_label = QLabel(description)
        desc_label.setFont(QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_BODY_SMALL))
        desc_label.setStyleSheet(f"color: {COLORS.TEXT_SECONDARY};")
        desc_label.setWordWrap(True)

        layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()

        self.setLayout(layout)


class SectionHeader(QWidget):
    """Section header widget with frozen design tokens.

    A reusable header component for organizing UI sections with clear
    visual hierarchy. All styling uses the frozen design system.

    Attributes:
        title: The section title
        description: Optional descriptive text
    """

    def __init__(self, title: str, description: str = ""):
        """Initialize a SectionHeader widget with frozen styling.

        Args:
            title: The section title text
            description: Optional description subtitle

        Note:
            All styling uses frozen design tokens from the design system.
        """
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, SPACING.SM)
        layout.setSpacing(SPACING.XS)

        # Title with frozen typography
        title_label = QLabel(title)
        title_label.setFont(QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_SECTION_HEADER, QFont.Bold))
        title_label.setStyleSheet(f"color: {COLORS.TEXT_PRIMARY};")

        layout.addWidget(title_label)

        # Optional description with frozen typography
        if description:
            desc_label = QLabel(description)
            desc_label.setFont(QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_BODY_SMALL))
            desc_label.setStyleSheet(f"color: {COLORS.TEXT_SECONDARY};")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        self.setLayout(layout)


class StatusIndicator(QWidget):
    """Frozen status indicator widget.

    Displays application status with icon and message.
    Uses frozen design tokens for consistent appearance.

    Attributes:
        message: Current status message
        status_type: Current status type (success, warning, error, info)
    """

    def __init__(self, message: str = "Ready to use", success: bool = True):
        """Initialize a StatusIndicator widget.

        Args:
            message: Initial status message
            success: True for success status, False for warning

        Note:
            Uses frozen design tokens for styling.
        """
        super().__init__()
        self.message = message
        self.success = success
        self.setup_ui()

    def setup_ui(self) -> None:
        """Setup status indicator UI with frozen design tokens."""
        from features.ui.design_system import BORDERS, SPACING

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS.BACKGROUND_CARD};
                border: {BORDERS.WIDTH_DEFAULT}px solid {COLORS.BORDER_DEFAULT};
                border-radius: {BORDERS.RADIUS_STATUS}px;
                padding: {SPACING.MD}px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(SPACING.MD, SPACING.MD, SPACING.MD, SPACING.MD)

        # Status icon
        self.icon_label = QLabel(ICONS.SUCCESS)
        self.icon_label.setFont(QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_STATUS_ICON, QFont.Bold))
        self.icon_label.setStyleSheet(StyleSheetTemplates.status_widget(self.success))

        # Status text
        self.message_label = QLabel(self.message)
        self.message_label.setFont(QFont(TYPOGRAPHY.FONT_FAMILY, TYPOGRAPHY.SIZE_BODY_NORMAL))
        self.message_label.setStyleSheet(f"color: {COLORS.TEXT_PRIMARY}; background: transparent;")

        layout.addWidget(self.icon_label)
        layout.addWidget(self.message_label)

        self.setLayout(layout)

    def update_status(self, message: str, success: bool = True) -> None:
        """Update status message and styling.

        Args:
            message: New status message
            success: True for success (green), False for warning (orange)

        Note:
            Uses frozen design tokens for status colors.
        """
        from features.ui.ui_config import StatusType

        self.message = message
        self.success = success

        # Update icon and styling based on frozen status types
        if success:
            icon = ICONS.SUCCESS
            color = COLORS.STATUS_SUCCESS
        else:
            icon = ICONS.WARNING
            color = COLORS.STATUS_WARNING

        self.icon_label.setText(icon)
        self.icon_label.setStyleSheet(f"color: {color}; background: transparent;")
        self.message_label.setText(message)

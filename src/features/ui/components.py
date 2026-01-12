"""Frozen UI Components for PC Utilities Manager.

This module provides reusable UI widgets that adhere to the frozen design system.
All components use immutable design tokens to ensure consistency.

IMPORTANT: These components are part of the frozen UI/UX v2.0 standard.
Modifications must maintain design system integrity.
"""

from typing import Callable, Optional
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QHBoxLayout,
    QStackedWidget,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from features.ui.design_system import (
    COLORS,
    TYPOGRAPHY,
    SPACING,
    BORDERS,
    ICONS,
    TABS,
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


class ModernTabBar(QWidget):
    """Modern tab bar widget with frozen design tokens.

    A horizontal tab bar that displays tabs with icons and labels.
    Uses frozen design tokens for consistent styling.

    Attributes:
        tabs: List of tab configuration dictionaries
        active_tab_id: ID of the currently active tab
    """

    tab_changed = Signal(str)  # Signal emitted when tab changes

    def __init__(self, tabs: list[dict], active_tab_id: str = "security"):
        """Initialize a ModernTabBar widget.

        Args:
            tabs: List of tab dictionaries with keys: id, title, icon
            active_tab_id: ID of the initially active tab

        Note:
            All styling uses frozen design tokens from the design system.
        """
        super().__init__()
        self.tabs = tabs
        self.active_tab_id = active_tab_id
        self.tab_buttons: dict[str, QPushButton] = {}
        self.setup_ui()

    def setup_ui(self) -> None:
        """Setup tab bar UI with frozen design tokens."""
        self.setStyleSheet(StyleSheetTemplates.tab_container())
        self.setFixedHeight(TABS.TAB_BAR_HEIGHT + SPACING.SM)

        layout = QHBoxLayout()
        layout.setContentsMargins(SPACING.MD, SPACING.SM, SPACING.MD, 0)
        layout.setSpacing(TABS.TAB_SPACING)

        # Create tab button for each tab
        for tab in self.tabs:
            tab_button = QPushButton(f"{tab['icon']} {tab['title']}")
            tab_id = tab['id']
            is_active = (tab_id == self.active_tab_id)

            tab_button.setStyleSheet(StyleSheetTemplates.tab_button(is_active))
            tab_button.setCursor(Qt.PointingHandCursor)
            tab_button.clicked.connect(lambda checked, tid=tab_id: self._on_tab_clicked(tid))

            self.tab_buttons[tab_id] = tab_button
            layout.addWidget(tab_button)

        layout.addStretch()
        self.setLayout(layout)

    def _on_tab_clicked(self, tab_id: str) -> None:
        """Handle tab button click.

        Args:
            tab_id: ID of the clicked tab
        """
        if tab_id != self.active_tab_id:
            self.set_active_tab(tab_id)
            self.tab_changed.emit(tab_id)

    def set_active_tab(self, tab_id: str) -> None:
        """Set the active tab and update styling.

        Args:
            tab_id: ID of the tab to set as active

        Raises:
            ValueError: If tab_id is not found in tabs
        """
        if tab_id not in self.tab_buttons:
            raise ValueError(f"Unknown tab ID: {tab_id}")

        # Update old active tab button
        old_button = self.tab_buttons[self.active_tab_id]
        old_button.setStyleSheet(StyleSheetTemplates.tab_button(False))

        # Update new active tab button
        self.active_tab_id = tab_id
        new_button = self.tab_buttons[tab_id]
        new_button.setStyleSheet(StyleSheetTemplates.tab_button(True))


class ModernTabWidget(QWidget):
    """Modern tab widget with frozen design tokens.

    A complete tab widget with tab bar and content area.
    Manages switching between tab content using a stacked widget.

    Attributes:
        tabs: List of tab configuration dictionaries
        active_tab_id: ID of the currently active tab
        tab_contents: Dictionary mapping tab IDs to content widgets
    """

    tab_changed = Signal(str)  # Signal emitted when tab changes

    def __init__(self, tabs: list[dict], active_tab_id: str = "security"):
        """Initialize a ModernTabWidget widget.

        Args:
            tabs: List of tab dictionaries with keys: id, title, icon
            active_tab_id: ID of the initially active tab

        Note:
            All styling uses frozen design tokens from the design system.
        """
        super().__init__()
        self.tabs = tabs
        self.active_tab_id = active_tab_id
        self.tab_contents: dict[str, QWidget] = {}
        self.setup_ui()

    def setup_ui(self) -> None:
        """Setup tab widget UI with frozen design tokens."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create tab bar
        self.tab_bar = ModernTabBar(self.tabs, self.active_tab_id)
        self.tab_bar.tab_changed.connect(self._on_tab_changed)
        layout.addWidget(self.tab_bar)

        # Create stacked widget for content
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet(StyleSheetTemplates.tab_content_area())
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)

    def _on_tab_changed(self, tab_id: str) -> None:
        """Handle tab change from tab bar.

        Args:
            tab_id: ID of the newly active tab
        """
        self.active_tab_id = tab_id

        # Switch content widget
        if tab_id in self.tab_contents:
            self.stacked_widget.setCurrentWidget(self.tab_contents[tab_id])

        self.tab_changed.emit(tab_id)

    def add_tab_content(self, tab_id: str, content: QWidget) -> None:
        """Add content widget for a tab.

        Args:
            tab_id: ID of the tab
            content: Widget to display as tab content

        Raises:
            ValueError: If tab_id is not found in tabs
        """
        if tab_id not in [t['id'] for t in self.tabs]:
            raise ValueError(f"Unknown tab ID: {tab_id}")

        # Add to stacked widget if not already added
        if tab_id not in self.tab_contents:
            self.tab_contents[tab_id] = content
            self.stacked_widget.addWidget(content)

            # Set as current if this is the active tab
            if tab_id == self.active_tab_id:
                self.stacked_widget.setCurrentWidget(content)

    def get_active_tab_id(self) -> str:
        """Get the ID of the currently active tab.

        Returns:
            Active tab ID
        """
        return self.active_tab_id

    def set_active_tab(self, tab_id: str) -> None:
        """Set the active tab programmatically.

        Args:
            tab_id: ID of the tab to set as active
        """
        self.tab_bar.set_active_tab(tab_id)


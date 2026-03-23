"""Status indicator component for PC Utilities Manager.

This module provides the status indicator widget that displays
application status with icon and message.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont

from features.ui.design_system import COLORS, SPACING, BORDERS, ICONS


class StatusIndicatorWidget(QWidget):
    """Modern status indicator widget with frozen design tokens.

    Displays application status with icon and message.
    Uses frozen design tokens for consistent appearance.

    Signals:
        status_changed: Emitted when status is updated (message, success)
    """

    status_changed = Signal(str, bool)

    def __init__(self, message: str = "Ready to use", success: bool = True, parent=None):
        """Initialize a StatusIndicatorWidget.

        Args:
            message: Initial status message
            success: True for success status, False for warning
            parent: Optional parent widget
        """
        super().__init__(parent)
        self.message = message
        self.success = success
        self._init_ui()

    def _init_ui(self) -> None:
        """Setup status indicator UI with frozen design tokens."""
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
        self.status_icon = QLabel(ICONS.SUCCESS)
        self.status_icon.setFont(
            QFont("Segoe UI", 16, QFont.Bold)
        )
        self.status_icon.setStyleSheet(
            f"color: {COLORS.STATUS_SUCCESS}; background: transparent;"
        )

        # Status text
        self.status_label = QLabel(self.message)
        self.status_label.setFont(QFont("Segoe UI", 11))
        self.status_label.setStyleSheet(
            f"color: {COLORS.TEXT_PRIMARY}; background: transparent;"
        )

        layout.addWidget(self.status_icon)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def update_status(self, message: str, success: bool = True) -> None:
        """Update status indicator with message.

        Args:
            message: Status message to display
            success: True for success (green), False for warning (orange)
        """
        self.message = message
        self.success = success

        icon = ICONS.SUCCESS if success else ICONS.WARNING
        color = COLORS.STATUS_SUCCESS if success else COLORS.STATUS_WARNING

        self.status_icon.setText(icon)
        self.status_icon.setStyleSheet(f"color: {color}; background: transparent;")
        self.status_label.setText(message)

        # Emit signal for other components
        self.status_changed.emit(message, success)

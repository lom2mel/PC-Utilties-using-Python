"""Tests for status indicator component."""

import pytest
from PySide6.QtCore import QObject

from features.ui.windows.status_indicator import StatusIndicatorWidget


class TestStatusIndicator:
    """Tests for status indicator component."""

    def test_create_status_indicator_default(self, qtbot):
        """Test that status indicator is created with default values."""
        indicator = StatusIndicatorWidget()

        # Verify indicator is created
        assert indicator is not None
        assert indicator.message == "Ready to use"
        assert indicator.success is True

        # Verify UI elements exist
        assert indicator.status_icon is not None
        assert indicator.status_label is not None

    def test_create_status_indicator_custom(self, qtbot):
        """Test that status indicator can be created with custom values."""
        custom_message = "Custom message"
        indicator = StatusIndicatorWidget(message=custom_message, success=False)

        # Verify indicator is created with custom values
        assert indicator.message == custom_message
        assert indicator.success is False

    def test_update_status_success(self, qtbot):
        """Test that status can be updated with success state."""
        indicator = StatusIndicatorWidget()
        indicator.update_status("Operation complete", success=True)

        # Verify status is updated
        assert indicator.message == "Operation complete"
        assert indicator.success is True

    def test_update_status_warning(self, qtbot):
        """Test that status can be updated with warning state."""
        indicator = StatusIndicatorWidget()
        indicator.update_status("Operation failed", success=False)

        # Verify status is updated
        assert indicator.message == "Operation failed"
        assert indicator.success is False

    def test_status_changed_signal(self, qtbot):
        """Test that status_changed signal is emitted."""
        indicator = StatusIndicatorWidget()

        # Track signal emissions
        received = []
        indicator.status_changed.connect(lambda msg, success: received.append((msg, success)))

        # Update status
        indicator.update_status("Test message", success=True)

        # Verify signal was emitted
        assert len(received) == 1
        assert received[0] == ("Test message", True)

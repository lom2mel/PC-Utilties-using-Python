"""Integration tests for frozen UI system."""

import pytest

from features.ui.design_system import COLORS
from features.ui.ui_config import CONFIG
from features.ui.state_manager import (
    StateManager,
    UIState,
    OperationType,
)


class TestFrozenUIIntegration:
    """Integration tests for frozen UI system."""

    def test_config_and_design_system_consistency(self):
        """Test that config aligns with design system."""
        # Feature colors should match design system colors
        assert CONFIG.features.AVAST.accent_color == "#FF6600"
        assert CONFIG.features.AVAST.accent_color == COLORS.AVAST_ORANGE

    def test_state_and_config_integration(self):
        """Test that state management works with config."""
        manager = StateManager()

        # Use config default message
        manager.update_status(CONFIG.status.default_message)
        assert manager.get_state().status_message == CONFIG.status.default_message

    def test_complete_state_transition_flow(self):
        """Test complete state transition workflow."""
        manager = StateManager()

        # Start: IDLE
        assert manager.get_state().ui_state == UIState.IDLE

        # Begin operation: BUSY
        manager.start_operation(OperationType.CONVERT_OFFICE)
        assert manager.get_state().ui_state == UIState.BUSY

        # Update progress
        manager.update_operation_progress(0.5)
        assert manager.get_state().operation_progress == 0.5

        # Complete operation
        manager.end_operation()
        manager.update_status("Conversion complete")
        assert manager.get_state().ui_state == UIState.IDLE

"""Tests for state management."""

import pytest

from features.ui.state_manager import (
    ApplicationState,
    StateManager,
    UIState,
    OperationType,
    OperationContext,
    get_state_manager,
    validate_state_integrity,
)
from features.ui.ui_config import StatusType, InteractionMode


class TestTabStateManagement:
    """Test tab state management."""

    def test_default_active_tab(self, sample_state):
        """Test that default active tab is security."""
        assert sample_state.active_tab_id == "security"

    def test_with_tab_creates_new_state(self, sample_state):
        """Test that with_tab creates new state."""
        new_state = sample_state.with_tab("converters")

        assert new_state.active_tab_id == "converters"
        # Original state unchanged
        assert sample_state.active_tab_id == "security"

    def test_with_tab_validates_tab_id(self, sample_state):
        """Test that with_tab validates tab ID."""
        # Invalid tab ID should raise ValueError
        with pytest.raises(ValueError):
            sample_state.with_tab("invalid_tab")

    def test_state_manager_switch_tab(self, state_manager):
        """Test StateManager switch_tab method."""
        # Default tab should be security
        assert state_manager.get_active_tab_id() == "security"

        # Switch to converters
        state_manager.switch_tab("converters")
        assert state_manager.get_active_tab_id() == "converters"

    def test_state_manager_switch_invalid_tab(self, state_manager):
        """Test StateManager switch_tab with invalid tab."""
        # Invalid tab should raise ValueError
        with pytest.raises(ValueError):
            state_manager.switch_tab("invalid_tab")


class TestApplicationState:
    """Test ApplicationState immutability and transitions."""

    def test_state_is_frozen(self, sample_state):
        """Test that state is immutable."""
        with pytest.raises(Exception):  # FrozenInstanceError or similar
            sample_state.status_message = "New Message"

    def test_with_status_creates_new_state(self, sample_state):
        """Test that with_status creates new state."""
        new_state = sample_state.with_status("New message", StatusType.WARNING)

        assert new_state.status_message == "New message"
        assert new_state.status_type == StatusType.WARNING
        # Original state unchanged
        assert sample_state.status_message == "Test"
        assert sample_state.status_type == StatusType.SUCCESS

    def test_with_ui_state_creates_new_state(self, sample_state):
        """Test that with_ui_state creates new state."""
        new_state = sample_state.with_ui_state(UIState.BUSY)

        assert new_state.ui_state == UIState.BUSY
        # Original unchanged
        assert sample_state.ui_state == UIState.IDLE

    def test_with_operation_creates_busy_state(self, sample_state):
        """Test that with_operation sets busy state."""
        new_state = sample_state.with_operation(OperationType.CONVERT_OFFICE)

        assert new_state.ui_state == UIState.BUSY
        assert new_state.mode == InteractionMode.BUSY
        assert new_state.active_operation == OperationType.CONVERT_OFFICE

    def test_with_operation_validates_progress(self, sample_state):
        """Test that progress validation works."""
        # Valid progress
        new_state = sample_state.with_operation(OperationType.DOWNLOAD, progress=0.5)
        assert new_state.operation_progress == 0.5

        # Invalid progress (too high)
        with pytest.raises(ValueError):
            sample_state.with_operation(OperationType.DOWNLOAD, progress=1.5)

        # Invalid progress (too low)
        with pytest.raises(ValueError):
            sample_state.with_operation(OperationType.DOWNLOAD, progress=-0.1)


class TestStateManager:
    """Test StateManager thread safety and functionality."""

    def test_get_state(self, state_manager):
        """Test getting current state."""
        state = state_manager.get_state()
        assert isinstance(state, ApplicationState)
        assert state.ui_state == UIState.IDLE
        assert state.mode == InteractionMode.NORMAL

    def test_set_state(self, state_manager):
        """Test setting new state."""
        new_state = state_manager.get_state().with_status("New status")
        state_manager.set_state(new_state)

        assert state_manager.get_state().status_message == "New status"

    def test_update_status(self, state_manager):
        """Test convenience method for updating status."""
        state_manager.update_status("Processing...", success=False)

        state = state_manager.get_state()
        assert state.status_message == "Processing..."
        assert state.status_type == StatusType.WARNING

    def test_start_and_end_operation(self, state_manager):
        """Test operation lifecycle."""
        # Start operation
        state_manager.start_operation(OperationType.CONVERT_IMAGE)
        assert state_manager.is_busy()
        assert state_manager.get_state().active_operation == OperationType.CONVERT_IMAGE

        # End operation
        state_manager.end_operation()
        assert not state_manager.is_busy()
        assert state_manager.get_state().active_operation is None

    def test_get_mode(self, state_manager):
        """Test getting current mode."""
        assert state_manager.get_mode() == InteractionMode.NORMAL

    def test_state_history(self, state_manager):
        """Test that state history is tracked."""
        # Make several state changes
        for i in range(5):
            state_manager.update_status(f"Status {i}")

        history = state_manager.get_history()
        assert len(history) == 5


class TestOperationContext:
    """Test OperationContext for automatic state management."""

    def test_successful_operation(self, state_manager):
        """Test context manager on success."""
        with OperationContext(OperationType.CONVERT_OFFICE, "Converting...", state_manager):
            assert state_manager.is_busy()
            assert state_manager.get_state().active_operation == OperationType.CONVERT_OFFICE

        # After context, operation should be complete
        assert not state_manager.is_busy()

    def test_failed_operation(self, state_manager):
        """Test context manager on error."""
        with pytest.raises(ValueError):
            with OperationContext(OperationType.CONVERT_OFFICE, "Converting...", state_manager):
                raise ValueError("Conversion failed")

        # After error, operation should be complete but status should show error
        assert not state_manager.is_busy()
        assert "Error" in state_manager.get_state().status_message


class TestGlobalStateManager:
    """Test global state manager singleton."""

    def test_get_state_manager_returns_instance(self):
        """Test that get_state_manager returns an instance."""
        manager = get_state_manager()
        assert isinstance(manager, StateManager)

    def test_get_state_manager_is_singleton(self):
        """Test that get_state_manager returns same instance."""
        manager1 = get_state_manager()
        manager2 = get_state_manager()
        assert manager1 is manager2


class TestStateValidation:
    """Test state management validation."""

    def test_validate_state_integrity(self):
        """Test that state integrity validation passes."""
        assert validate_state_integrity() is True

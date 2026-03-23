"""Shared fixtures for frozen UI tests."""

import pytest
from datetime import datetime, UTC

from features.ui.state_manager import (
    ApplicationState,
    StateManager,
    UIState,
    OperationType,
)
from features.ui.ui_config import StatusType, InteractionMode


@pytest.fixture
def sample_state():
    """Provide a sample application state for testing."""
    return ApplicationState(
        ui_state=UIState.IDLE,
        mode=InteractionMode.NORMAL,
        status_message="Test",
        status_type=StatusType.SUCCESS,
    )


@pytest.fixture
def state_manager():
    """Provide a StateManager instance for testing."""
    return StateManager()


@pytest.fixture
def sample_datetime():
    """Provide a sample datetime for testing."""
    return datetime.now(UTC)

"""Frozen State Management for PC Utilities Manager UI.

This module provides immutable state management patterns for the UI.
All state changes follow strict patterns to ensure consistency.

The frozen state principle:
- State is immutable (cannot be changed after creation)
- State changes create new state instances
- State transitions are validated and controlled
- All state is tracked and auditable
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Final, Optional, Dict, Any
from threading import Lock

from features.ui.ui_config import InteractionMode, StatusType, UIStateConstants


# =============================================================================
# STATE ENUMS - FROZEN
# =============================================================================

class UIState(Enum):
    """Frozen enum of valid UI states.

    The application can only be in one of these states at any time.
    """
    IDLE = auto()
    BUSY = auto()
    ERROR = auto()
    SUCCESS = auto()


class OperationType(Enum):
    """Frozen enum of operation types.

    All long-running operations must be one of these types.
    """
    DOWNLOAD = auto()
    CONVERT_OFFICE = auto()
    CONVERT_IMAGE = auto()
    SCAN = auto()


# =============================================================================
# IMMUTABLE STATE DATA CLASSES
# =============================================================================

@dataclass(frozen=True)
class ApplicationState:
    """Immutable snapshot of application state.

    All attributes are read-only. To change state, create a new instance.
    This ensures state changes are explicit and trackable.

    Attributes:
        ui_state: Current UI state
        mode: Current interaction mode
        status_message: Current status message
        status_type: Current status type
        timestamp: When this state was created
        active_operation: Currently running operation (if any)
    """

    ui_state: UIState
    mode: InteractionMode
    status_message: str
    status_type: StatusType
    timestamp: datetime = field(default_factory=datetime.now)
    active_operation: Optional[OperationType] = None
    operation_progress: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def with_status(
        self,
        message: str,
        status_type: StatusType = StatusType.SUCCESS
    ) -> "ApplicationState":
        """Create a new state with updated status.

        Args:
            message: New status message
            status_type: New status type

        Returns:
            New ApplicationState instance with updated status
        """
        return ApplicationState(
            ui_state=self.ui_state,
            mode=self.mode,
            status_message=message,
            status_type=status_type,
            timestamp=datetime.now(),
            active_operation=self.active_operation,
            operation_progress=self.operation_progress,
            metadata=dict(self.metadata),  # Create a copy
        )

    def with_ui_state(self, ui_state: UIState) -> "ApplicationState":
        """Create a new state with updated UI state.

        Args:
            ui_state: New UI state

        Returns:
            New ApplicationState instance with updated UI state
        """
        return ApplicationState(
            ui_state=ui_state,
            mode=self.mode,
            status_message=self.status_message,
            status_type=self.status_type,
            timestamp=datetime.now(),
            active_operation=self.active_operation,
            operation_progress=self.operation_progress,
            metadata=dict(self.metadata),
        )

    def with_mode(self, mode: InteractionMode) -> "ApplicationState":
        """Create a new state with updated interaction mode.

        Args:
            mode: New interaction mode

        Returns:
            New ApplicationState instance with updated mode

        Raises:
            ValueError: If mode transition is not allowed
        """
        # Validate state transition
        constants = UIStateConstants()
        if mode != self.mode:
            allowed = constants.ALLOWED_TRANSITIONS.get(self.mode, tuple())
            if mode not in allowed and self.mode not in (InteractionMode.NORMAL,):
                raise ValueError(
                    f"Cannot transition from {self.mode} to {mode}. "
                    f"Allowed transitions: {allowed}"
                )

        return ApplicationState(
            ui_state=self.ui_state,
            mode=mode,
            status_message=self.status_message,
            status_type=self.status_type,
            timestamp=datetime.now(),
            active_operation=self.active_operation,
            operation_progress=self.operation_progress,
            metadata=dict(self.metadata),
        )

    def with_operation(
        self,
        operation: Optional[OperationType],
        progress: float = 0.0
    ) -> "ApplicationState":
        """Create a new state with active operation.

        Args:
            operation: Operation type (None if no operation)
            progress: Operation progress (0.0 to 1.0)

        Returns:
            New ApplicationState instance with operation

        Raises:
            ValueError: If progress is out of range
        """
        if not 0.0 <= progress <= 1.0:
            raise ValueError(f"Progress must be between 0.0 and 1.0, got {progress}")

        return ApplicationState(
            ui_state=UIState.BUSY if operation else UIState.IDLE,
            mode=InteractionMode.BUSY if operation else InteractionMode.NORMAL,
            status_message=self.status_message,
            status_type=self.status_type,
            timestamp=datetime.now(),
            active_operation=operation,
            operation_progress=progress,
            metadata=dict(self.metadata),
        )


# =============================================================================
# STATE MANAGER - FROZEN PATTERN
# =============================================================================

class StateManager:
    """Thread-safe manager for immutable application state.

    The StateManager ensures:
    - All state changes are thread-safe
    - State history is tracked for debugging
    - State transitions are validated
    - No direct mutation of state

    Usage:
        manager = StateManager()
        current_state = manager.get_state()
        new_state = current_state.with_status("Processing...", StatusType.INFO)
        manager.set_state(new_state)
    """

    def __init__(self):
        """Initialize the state manager with default state."""
        self._state: ApplicationState = ApplicationState(
            ui_state=UIState.IDLE,
            mode=InteractionMode.NORMAL,
            status_message="Ready to use",
            status_type=StatusType.SUCCESS,
        )
        self._lock: Lock = Lock()
        self._history: list[ApplicationState] = []
        self._max_history: int = 100

    def get_state(self) -> ApplicationState:
        """Get current application state (thread-safe).

        Returns:
            Current ApplicationState instance
        """
        with self._lock:
            return self._state

    def set_state(self, new_state: ApplicationState) -> None:
        """Set new application state (thread-safe).

        Args:
            new_state: New state to set

        Note:
            Adds state to history for debugging/auditing
        """
        with self._lock:
            # Add to history
            self._history.append(self._state)
            # Limit history size
            if len(self._history) > self._max_history:
                self._history.pop(0)

            # Set new state
            self._state = new_state

    def update_status(self, message: str, success: bool = True) -> None:
        """Update status message (convenience method).

        Args:
            message: New status message
            success: True for success, False for warning/error
        """
        status_type = StatusType.SUCCESS if success else StatusType.WARNING
        current = self.get_state()
        new_state = current.with_status(message, status_type)
        self.set_state(new_state)

    def start_operation(self, operation: OperationType) -> None:
        """Start a long-running operation.

        Args:
            operation: Type of operation starting
        """
        current = self.get_state()
        new_state = current.with_operation(operation, progress=0.0)
        self.set_state(new_state)

    def update_operation_progress(self, progress: float) -> None:
        """Update operation progress.

        Args:
            progress: Progress value (0.0 to 1.0)
        """
        current = self.get_state()
        if current.active_operation:
            new_state = current.with_operation(current.active_operation, progress)
            self.set_state(new_state)

    def end_operation(self) -> None:
        """End the current operation."""
        current = self.get_state()
        new_state = current.with_operation(None, progress=0.0)
        self.set_state(new_state)

    def get_history(self) -> list[ApplicationState]:
        """Get state history (thread-safe).

        Returns:
            List of previous states (most recent last)
        """
        with self._lock:
            return list(self._history)

    def is_busy(self) -> bool:
        """Check if application is busy.

        Returns:
            True if an operation is in progress
        """
        return self.get_state().active_operation is not None

    def get_mode(self) -> InteractionMode:
        """Get current interaction mode.

        Returns:
            Current InteractionMode
        """
        return self.get_state().mode


# =============================================================================
# GLOBAL STATE MANAGER INSTANCE
# =============================================================================

# Global state manager instance (singleton pattern)
_state_manager: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    """Get the global state manager instance.

    Returns:
        Global StateManager instance

    Note:
        Creates the instance on first call (lazy initialization)
    """
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager


# =============================================================================
# STATE TRANSITION CONTEXT MANAGER
# =============================================================================

class OperationContext:
    """Context manager for automatic state management during operations.

    Ensures operations properly update state and handle errors.

    Usage:
        with OperationContext(OperationType.CONVERT_OFFICE, "Converting files..."):
            # Do conversion work
            pass

    The context manager will:
    1. Set busy state on entry
    2. Update status message
    3. Handle errors and update state appropriately
    4. Clear busy state on exit
    """

    def __init__(
        self,
        operation: OperationType,
        status_message: str,
        state_manager: Optional[StateManager] = None
    ):
        """Initialize operation context.

        Args:
            operation: Type of operation
            status_message: Status message to display
            state_manager: State manager to use (defaults to global)
        """
        self.operation = operation
        self.status_message = status_message
        self.state_manager = state_manager or get_state_manager()
        self.success = True

    def __enter__(self) -> "OperationContext":
        """Enter operation context."""
        self.state_manager.start_operation(self.operation)
        self.state_manager.update_status(self.status_message, success=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit operation context."""
        self.state_manager.end_operation()

        if exc_type is not None:
            # Operation failed
            self.state_manager.update_status(
                f"Error: {str(exc_val)}",
                success=False
            )
            return False  # Re-raise exception

        # Operation succeeded
        return True


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_state_integrity() -> bool:
    """Validate that state management is working correctly.

    Returns:
        True if state management is valid
    """
    manager = get_state_manager()

    # Test state creation
    state = ApplicationState(
        ui_state=UIState.IDLE,
        mode=InteractionMode.NORMAL,
        status_message="Test",
        status_type=StatusType.SUCCESS,
    )

    # Test immutability
    try:
        state.ui_state = UIState.BUSY
        return False  # Should not be able to modify
    except (AttributeError, NotImplementedError):
        pass  # Expected - frozen dataclass

    # Test state transitions
    new_state = state.with_status("New message")
    assert new_state.status_message == "New message"
    assert state.status_message == "Test"  # Original unchanged

    # Test state manager
    manager.set_state(new_state)
    assert manager.get_state().status_message == "New message"

    return True


# Auto-validate on import
if not validate_state_integrity():
    raise RuntimeError("State management validation failed")

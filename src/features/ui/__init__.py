"""Frozen UI system for PC Utilities Manager v2.0.

This package provides the frozen design system, configuration, and state
management for the application's user interface.

The UI/UX is frozen as of version 2.0, meaning all design tokens and
configuration values are immutable and validated.

Modules:
    design_system: Frozen design tokens (colors, typography, spacing, etc.)
    ui_config: Frozen UI configuration and feature registry
    state_manager: Immutable state management patterns
    components: UI components using frozen design tokens
    modern_main_window: Main application window

Usage:
    from features.ui.design_system import COLORS, TYPOGRAPHY, SPACING
    from features.ui.ui_config import CONFIG
    from features.ui.state_manager import get_state_manager

    # Use frozen design tokens
    widget.setStyleSheet(f"background-color: {COLORS.BACKGROUND_CARD};")

    # Access frozen configuration
    feature = CONFIG.get_feature_by_name("AVAST")

    # Manage immutable state
    state_manager = get_state_manager()
    state_manager.update_status("Processing...", success=True)
"""

from features.ui.design_system import (
    COLORS,
    TYPOGRAPHY,
    SPACING,
    BORDERS,
    LAYOUT,
    ICONS,
    StyleSheetTemplates,
    validate_design_system,
)

from features.ui.ui_config import (
    CONFIG,
    StatusType,
    InteractionMode,
    FeatureCardConfig,
    MenuConfig,
    AboutDialogConfig,
    validate_config,
)

from features.ui.state_manager import (
    ApplicationState,
    StateManager,
    UIState,
    OperationType,
    OperationContext,
    get_state_manager,
    validate_state_integrity,
)

from features.ui.components import ModernCard, SectionHeader, StatusIndicator

__all__ = [
    # Design system
    "COLORS",
    "TYPOGRAPHY",
    "SPACING",
    "BORDERS",
    "LAYOUT",
    "ICONS",
    "StyleSheetTemplates",
    "validate_design_system",
    # Configuration
    "CONFIG",
    "StatusType",
    "InteractionMode",
    "FeatureCardConfig",
    "MenuConfig",
    "AboutDialogConfig",
    "validate_config",
    # State management
    "ApplicationState",
    "StateManager",
    "UIState",
    "OperationType",
    "OperationContext",
    "get_state_manager",
    "validate_state_integrity",
    # Components
    "ModernCard",
    "SectionHeader",
    "StatusIndicator",
]

# Validate frozen UI system on import
validate_design_system()
validate_config()
validate_state_integrity()

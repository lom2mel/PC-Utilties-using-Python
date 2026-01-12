"""Tests for frozen UI patterns in PC Utilities Manager.

This test suite validates:
- Design system immutability
- UI configuration integrity
- State management consistency
- Component adherence to frozen tokens
- Tab widget functionality

Run with: uv run pytest src/features/ui/tests/test_frozen_ui.py -v
"""

import pytest
from dataclasses import FrozenInstanceError

from features.ui.design_system import (
    COLORS,
    TYPOGRAPHY,
    SPACING,
    BORDERS,
    LAYOUT,
    ICONS,
    TABS,
    StyleSheetTemplates,
    validate_design_system,
)
from features.ui.ui_config import (
    CONFIG,
    StatusType,
    InteractionMode,
    FeatureCardConfig,
    TabConfig,
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


# =============================================================================
# DESIGN SYSTEM TESTS
# =============================================================================

class TestDesignSystemImmutability:
    """Test that design system tokens are immutable."""

    def test_colors_are_frozen(self):
        """Test that color palette dataclass is frozen."""
        # Should not be able to modify attributes
        with pytest.raises(FrozenInstanceError):
            COLORS.GRADIENT_START = "#000000"

    def test_colors_have_valid_format(self):
        """Test that all colors are valid hex codes."""
        for attr in dir(COLORS):
            if not attr.startswith('_'):
                color = getattr(COLORS, attr)
                assert isinstance(color, str)
                assert len(color) == 7
                assert color.startswith('#')
                # Verify it's a valid hex color
                int(color[1:], 16)  # Will raise if invalid

    def test_typography_is_frozen(self):
        """Test that typography tokens are frozen."""
        with pytest.raises(FrozenInstanceError):
            TYPOGRAPHY.FONT_FAMILY = "Arial"

    def test_spacing_is_frozen(self):
        """Test that spacing tokens are frozen."""
        with pytest.raises(FrozenInstanceError):
            SPACING.UNIT = 5

    def test_borders_is_frozen(self):
        """Test that border tokens are frozen."""
        with pytest.raises(FrozenInstanceError):
            BORDERS.RADIUS_CARD = 15

    def test_layout_is_frozen(self):
        """Test that layout tokens are frozen."""
        with pytest.raises(FrozenInstanceError):
            LAYOUT.WINDOW_MIN_WIDTH = 1000

    def test_icons_is_frozen(self):
        """Test that icon tokens are frozen."""
        with pytest.raises(FrozenInstanceError):
            ICONS.SUCCESS = "OK"

    def test_tabs_is_frozen(self):
        """Test that tab tokens are frozen."""
        with pytest.raises(FrozenInstanceError):
            TABS.TAB_BAR_HEIGHT = 60


class TestDesignSystemValidation:
    """Test design system validation."""

    def test_validate_design_system(self):
        """Test that design system validation passes."""
        assert validate_design_system() is True

    def test_color_consistency(self):
        """Test that related colors are consistent."""
        # Gradient colors should be different
        assert COLORS.GRADIENT_START != COLORS.GRADIENT_END

        # Status colors should be distinct
        assert COLORS.STATUS_SUCCESS != COLORS.STATUS_WARNING
        assert COLORS.STATUS_WARNING != COLORS.STATUS_ERROR

    def test_spacing_progression(self):
        """Test that spacing values progress logically."""
        assert SPACING.XS < SPACING.SM < SPACING.MD < SPACING.LG < SPACING.XL


class TestStyleSheetTemplates:
    """Test stylesheet template generation."""

    def test_base_widget_template(self):
        """Test base widget stylesheet."""
        css = StyleSheetTemplates.base_widget()
        assert 'background-color' in css
        assert COLORS.BACKGROUND_PRIMARY in css

    def test_header_widget_template(self):
        """Test header widget stylesheet."""
        css = StyleSheetTemplates.header_widget()
        assert 'qlineargradient' in css
        assert COLORS.GRADIENT_START in css
        assert COLORS.GRADIENT_END in css

    def test_card_widget_template(self):
        """Test card widget stylesheet with accent color."""
        css = StyleSheetTemplates.card_widget("#FF6600")
        assert 'ModernCard' in css
        assert '#FF6600' in css
        assert COLORS.BACKGROUND_CARD in css

    def test_status_widget_template(self):
        """Test status widget stylesheet."""
        css_success = StyleSheetTemplates.status_widget(True)
        css_warning = StyleSheetTemplates.status_widget(False)
        assert COLORS.STATUS_SUCCESS in css_success
        assert COLORS.STATUS_WARNING in css_warning

    def test_tab_container_template(self):
        """Test tab container stylesheet."""
        css = StyleSheetTemplates.tab_container()
        assert 'background-color' in css
        assert TABS.TAB_CONTAINER_BACKGROUND in css

    def test_tab_button_template_active(self):
        """Test active tab button stylesheet."""
        css = StyleSheetTemplates.tab_button(is_active=True)
        assert TABS.TAB_INDICATOR_COLOR in css
        assert TABS.TAB_TEXT_ACTIVE in css

    def test_tab_button_template_inactive(self):
        """Test inactive tab button stylesheet."""
        css = StyleSheetTemplates.tab_button(is_active=False)
        assert TABS.TAB_TEXT_INACTIVE in css
        assert 'hover' in css

    def test_tab_content_area_template(self):
        """Test tab content area stylesheet."""
        css = StyleSheetTemplates.tab_content_area()
        assert 'background-color' in css
        assert 'transparent' in css


# =============================================================================
# UI CONFIGURATION TESTS
# =============================================================================

class TestUIConfiguration:
    """Test UI configuration immutability and integrity."""

    def test_config_is_frozen(self):
        """Test that configuration is frozen."""
        with pytest.raises(FrozenInstanceError):
            CONFIG.window.title = "New Title"

    def test_validate_config(self):
        """Test that configuration validation passes."""
        assert validate_config() is True

    def test_get_feature_by_name(self):
        """Test retrieving feature configuration."""
        avast = CONFIG.get_feature_by_name("AVAST")
        assert isinstance(avast, FeatureCardConfig)
        assert avast.title == "Avast Antivirus"
        assert avast.icon == "🛡️"

    def test_get_feature_by_name_case_insensitive(self):
        """Test feature retrieval is case-insensitive."""
        feature1 = CONFIG.get_feature_by_name("avast")
        feature2 = CONFIG.get_feature_by_name("AVAST")
        feature3 = CONFIG.get_feature_by_name("Avast")
        assert feature1 == feature2 == feature3

    def test_get_feature_by_name_invalid(self):
        """Test that invalid feature name raises error."""
        with pytest.raises(AttributeError):
            CONFIG.get_feature_by_name("INVALID_FEATURE")

    def test_get_all_features(self):
        """Test retrieving all features."""
        features = CONFIG.get_all_features()
        assert len(features) >= 6  # At least the base features
        assert "AVAST" in features
        assert "OFFICE_CONVERTER" in features

    def test_get_features_by_category(self):
        """Test filtering features by category."""
        security_features = CONFIG.get_features_by_category("security")
        assert all(f.category == "security" for f in security_features)
        assert len(security_features) >= 4

        converter_features = CONFIG.get_features_by_category("converter")
        assert all(f.category == "converter" for f in converter_features)
        assert len(converter_features) >= 2


class TestFeatureCardConfig:
    """Test feature card configuration."""

    def test_feature_config_immutability(self):
        """Test that feature configs are immutable."""
        avast = CONFIG.features.AVAST
        with pytest.raises(FrozenInstanceError):
            avast.title = "New Title"

    def test_feature_config_values(self):
        """Test feature config has correct values."""
        office = CONFIG.features.OFFICE_CONVERTER
        assert office.category == "converter"
        assert office.keyboard_shortcut == "Ctrl+O"


class TestTabConfiguration:
    """Test tab configuration."""

    def test_tab_config_exists(self):
        """Test that tab configuration is available."""
        assert hasattr(CONFIG, 'tabs')
        assert CONFIG.tabs is not None

    def test_security_tab_config(self):
        """Test security tab configuration."""
        security = CONFIG.tabs.SECURITY
        assert isinstance(security, TabConfig)
        assert security.id == "security"
        assert security.title == "Security"
        assert security.icon == ICONS.TAB_SECURITY
        assert security.category == "security"

    def test_converters_tab_config(self):
        """Test converters tab configuration."""
        converters = CONFIG.tabs.CONVERTERS
        assert isinstance(converters, TabConfig)
        assert converters.id == "converters"
        assert converters.title == "Files"
        assert converters.icon == ICONS.TAB_CONVERTERS
        assert converters.category == "converter"

    def test_tab_config_immutability(self):
        """Test that tab configs are immutable."""
        security = CONFIG.tabs.SECURITY
        with pytest.raises(FrozenInstanceError):
            security.title = "New Title"

    def test_get_all_tabs(self):
        """Test retrieving all tabs."""
        tabs = CONFIG.tabs.get_all_tabs()
        assert isinstance(tabs, list)
        assert len(tabs) == 2
        assert tabs[0]['id'] == 'security'
        assert tabs[1]['id'] == 'converters'

    def test_get_tab_by_category(self):
        """Test retrieving tab by category."""
        security_tab = CONFIG.tabs.get_tab_by_category("security")
        assert security_tab is not None
        assert security_tab.id == "security"

        converter_tab = CONFIG.tabs.get_tab_by_category("converter")
        assert converter_tab is not None
        assert converter_tab.id == "converters"

    def test_get_tab_by_invalid_category(self):
        """Test retrieving tab with invalid category."""
        invalid_tab = CONFIG.tabs.get_tab_by_category("invalid")
        assert invalid_tab is None


# =============================================================================
# TAB STATE MANAGEMENT TESTS
# =============================================================================

class TestTabStateManagement:
    """Test tab state management."""

    def test_default_active_tab(self):
        """Test that default active tab is security."""
        state = ApplicationState(
            ui_state=UIState.IDLE,
            mode=InteractionMode.NORMAL,
            status_message="Test",
            status_type=StatusType.SUCCESS,
        )
        assert state.active_tab_id == "security"

    def test_with_tab_creates_new_state(self):
        """Test that with_tab creates new state."""
        state = ApplicationState(
            ui_state=UIState.IDLE,
            mode=InteractionMode.NORMAL,
            status_message="Test",
            status_type=StatusType.SUCCESS,
        )

        new_state = state.with_tab("converters")

        assert new_state.active_tab_id == "converters"
        # Original state unchanged
        assert state.active_tab_id == "security"

    def test_with_tab_validates_tab_id(self):
        """Test that with_tab validates tab ID."""
        state = ApplicationState(
            ui_state=UIState.IDLE,
            mode=InteractionMode.NORMAL,
            status_message="Test",
            status_type=StatusType.SUCCESS,
        )

        # Invalid tab ID should raise ValueError
        with pytest.raises(ValueError):
            state.with_tab("invalid_tab")

    def test_state_manager_switch_tab(self):
        """Test StateManager switch_tab method."""
        manager = StateManager()

        # Default tab should be security
        assert manager.get_active_tab_id() == "security"

        # Switch to converters
        manager.switch_tab("converters")
        assert manager.get_active_tab_id() == "converters"

    def test_state_manager_switch_invalid_tab(self):
        """Test StateManager switch_tab with invalid tab."""
        manager = StateManager()

        # Invalid tab should raise ValueError
        with pytest.raises(ValueError):
            manager.switch_tab("invalid_tab")


# =============================================================================
# STATE MANAGEMENT TESTS
# =============================================================================

class TestApplicationState:
    """Test ApplicationState immutability and transitions."""

    def test_state_is_frozen(self):
        """Test that state is immutable."""
        state = ApplicationState(
            ui_state=UIState.IDLE,
            mode=InteractionMode.NORMAL,
            status_message="Test",
            status_type=StatusType.SUCCESS,
        )
        with pytest.raises(FrozenInstanceError):
            state.status_message = "New Message"

    def test_with_status_creates_new_state(self):
        """Test that with_status creates new state."""
        state = ApplicationState(
            ui_state=UIState.IDLE,
            mode=InteractionMode.NORMAL,
            status_message="Test",
            status_type=StatusType.SUCCESS,
        )

        new_state = state.with_status("New message", StatusType.WARNING)

        assert new_state.status_message == "New message"
        assert new_state.status_type == StatusType.WARNING
        # Original state unchanged
        assert state.status_message == "Test"
        assert state.status_type == StatusType.SUCCESS

    def test_with_ui_state_creates_new_state(self):
        """Test that with_ui_state creates new state."""
        state = ApplicationState(
            ui_state=UIState.IDLE,
            mode=InteractionMode.NORMAL,
            status_message="Test",
            status_type=StatusType.SUCCESS,
        )

        new_state = state.with_ui_state(UIState.BUSY)

        assert new_state.ui_state == UIState.BUSY
        # Original unchanged
        assert state.ui_state == UIState.IDLE

    def test_with_operation_creates_busy_state(self):
        """Test that with_operation sets busy state."""
        state = ApplicationState(
            ui_state=UIState.IDLE,
            mode=InteractionMode.NORMAL,
            status_message="Test",
            status_type=StatusType.SUCCESS,
        )

        new_state = state.with_operation(OperationType.CONVERT_OFFICE)

        assert new_state.ui_state == UIState.BUSY
        assert new_state.mode == InteractionMode.BUSY
        assert new_state.active_operation == OperationType.CONVERT_OFFICE

    def test_with_operation_validates_progress(self):
        """Test that progress validation works."""
        state = ApplicationState(
            ui_state=UIState.IDLE,
            mode=InteractionMode.NORMAL,
            status_message="Test",
            status_type=StatusType.SUCCESS,
        )

        # Valid progress
        new_state = state.with_operation(OperationType.DOWNLOAD, progress=0.5)
        assert new_state.operation_progress == 0.5

        # Invalid progress (too high)
        with pytest.raises(ValueError):
            state.with_operation(OperationType.DOWNLOAD, progress=1.5)

        # Invalid progress (too low)
        with pytest.raises(ValueError):
            state.with_operation(OperationType.DOWNLOAD, progress=-0.1)


class TestStateManager:
    """Test StateManager thread safety and functionality."""

    def test_get_state(self):
        """Test getting current state."""
        manager = StateManager()
        state = manager.get_state()
        assert isinstance(state, ApplicationState)
        assert state.ui_state == UIState.IDLE
        assert state.mode == InteractionMode.NORMAL

    def test_set_state(self):
        """Test setting new state."""
        manager = StateManager()
        new_state = manager.get_state().with_status("New status")
        manager.set_state(new_state)

        assert manager.get_state().status_message == "New status"

    def test_update_status(self):
        """Test convenience method for updating status."""
        manager = StateManager()
        manager.update_status("Processing...", success=False)

        state = manager.get_state()
        assert state.status_message == "Processing..."
        assert state.status_type == StatusType.WARNING

    def test_start_and_end_operation(self):
        """Test operation lifecycle."""
        manager = StateManager()

        # Start operation
        manager.start_operation(OperationType.CONVERT_IMAGE)
        assert manager.is_busy()
        assert manager.get_state().active_operation == OperationType.CONVERT_IMAGE

        # End operation
        manager.end_operation()
        assert not manager.is_busy()
        assert manager.get_state().active_operation is None

    def test_get_mode(self):
        """Test getting current mode."""
        manager = StateManager()
        assert manager.get_mode() == InteractionMode.NORMAL

    def test_state_history(self):
        """Test that state history is tracked."""
        manager = StateManager()

        # Make several state changes
        for i in range(5):
            manager.update_status(f"Status {i}")

        history = manager.get_history()
        assert len(history) == 5


class TestOperationContext:
    """Test OperationContext for automatic state management."""

    def test_successful_operation(self):
        """Test context manager on success."""
        manager = StateManager()

        with OperationContext(OperationType.CONVERT_OFFICE, "Converting..."):
            assert manager.is_busy()
            assert manager.get_state().active_operation == OperationType.CONVERT_OFFICE

        # After context, operation should be complete
        assert not manager.is_busy()

    def test_failed_operation(self):
        """Test context manager on error."""
        manager = StateManager()

        with pytest.raises(ValueError):
            with OperationContext(OperationType.CONVERT_OFFICE, "Converting..."):
                raise ValueError("Conversion failed")

        # After error, operation should be complete but status should show error
        assert not manager.is_busy()
        assert "Error" in manager.get_state().status_message


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


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

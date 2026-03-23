"""Tests for stylesheet template generation."""

import pytest

from features.ui.design_system import (
    COLORS,
    TABS,
    StyleSheetTemplates,
)


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

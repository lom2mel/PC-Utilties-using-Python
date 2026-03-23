"""Tests for design system immutability."""

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
)


class TestDesignSystemImmutability:
    """Test that design system tokens are immutable."""

    def test_colors_are_frozen(self):
        """Test that color palette dataclass is frozen."""
        # Should not be able to modify attributes
        with pytest.raises(FrozenInstanceError):
            COLORS.GRADIENT_START = "#000000"

    def test_colors_have_valid_format(self):
        """Test that all colors are valid color codes."""
        for attr in dir(COLORS):
            if not attr.startswith('_'):
                color = getattr(COLORS, attr)
                assert isinstance(color, str)
                # Check for hex format (#RRGGBB)
                if color.startswith('#'):
                    assert len(color) == 7
                    # Verify it's a valid hex color
                    int(color[1:], 16)  # Will raise if invalid
                # Check for rgba format
                elif color.startswith('rgba('):
                    assert color.endswith(')')
                # Check for rgb format
                elif color.startswith('rgb('):
                    assert color.endswith(')')

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

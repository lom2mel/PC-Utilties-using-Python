"""Tests for design system validation."""

import pytest

from features.ui.design_system import (
    COLORS,
    SPACING,
    StyleSheetTemplates,
    validate_design_system,
)


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

"""Tests for header component."""

import pytest
from unittest.mock import Mock

from features.ui.windows.header import create_header


class TestHeader:
    """Tests for header component creation."""

    def test_create_header_default(self, qtbot):
        """Test that header is created with default values."""
        header = create_header()

        # Verify header is created
        assert header is not None
        assert header.height() == 120
        assert header.layout() is not None

        # Verify header has gradient background
        style = header.styleSheet()
        assert "qlineargradient" in style
        assert "#667EEA" in style  # GRADIENT_START
        assert "#764BA2" in style  # GRADIENT_END

    def test_create_header_with_custom_title(self, qtbot):
        """Test that header can be created with custom title."""
        custom_title = "Custom Title"
        header = create_header(title=custom_title)

        # Verify header is created
        assert header is not None

        # Find title label
        labels = header.findChildren(type(header))
        assert len(labels) > 0

    def test_create_header_with_callback(self, qtbot):
        """Test that header can be created with about callback."""
        callback = Mock()
        header = create_header(on_about_clicked=callback)

        # Verify header is created
        assert header is not None

    def test_create_header_custom_subtitle(self, qtbot):
        """Test that header can be created with custom subtitle."""
        custom_subtitle = "Custom subtitle text"
        header = create_header(subtitle=custom_subtitle)

        # Verify header is created
        assert header is not None

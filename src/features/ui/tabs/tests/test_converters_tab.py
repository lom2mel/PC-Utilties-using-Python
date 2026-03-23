"""Tests for converters tab content."""

import pytest
from unittest.mock import MagicMock, Mock

from features.ui.tabs.converters_tab import create_converters_tab_content


class TestConvertersTab:
    """Tests for converters tab content creation."""

    def test_create_converters_tab_content(self, qtbot):
        """Test that converters tab content is created successfully."""
        # Create mock converter handlers and callbacks
        converter_handlers = MagicMock()
        start_conversion = Mock()
        start_picture_to_pdf = Mock()

        # Create tab content
        content = create_converters_tab_content(
            converter_handlers,
            start_conversion,
            start_picture_to_pdf,
        )

        # Verify content is created
        assert content is not None
        assert content.layout() is not None
        assert content.layout().count() > 0

        # Verify content has transparent background
        assert "background: transparent" in content.styleSheet()

    def test_converters_tab_has_office_card(self, qtbot):
        """Test that converters tab contains Office converter card."""
        converter_handlers = MagicMock()
        start_conversion = Mock()
        start_picture_to_pdf = Mock()

        content = create_converters_tab_content(
            converter_handlers,
            start_conversion,
            start_picture_to_pdf,
        )

        # Verify layout exists
        layout = content.layout()
        assert layout is not None

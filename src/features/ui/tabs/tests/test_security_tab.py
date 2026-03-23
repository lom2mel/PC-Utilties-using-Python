"""Tests for security tab content."""

import pytest
from unittest.mock import MagicMock, Mock

from features.ui.tabs.security_tab import create_security_tab_content
from features.ui.download_handlers import DownloadHandlers


class TestSecurityTab:
    """Tests for security tab content creation."""

    def test_create_security_tab_content(self, qtbot):
        """Test that security tab content is created successfully."""
        # Create mock download handlers
        download_handlers = MagicMock(spec=DownloadHandlers)
        download_handlers.download_avast = Mock()
        download_handlers.open_virustotal = Mock()
        download_handlers.download_ccleaner = Mock()
        download_handlers.download_speccy = Mock()
        download_handlers.download_bitdefender = Mock()

        # Create tab content
        content = create_security_tab_content(download_handlers)

        # Verify content is created
        assert content is not None
        assert content.layout() is not None
        assert content.layout().count() > 0

        # Verify content has transparent background
        assert "background: transparent" in content.styleSheet()

    def test_security_tab_has_cards(self, qtbot):
        """Test that security tab contains expected cards."""
        download_handlers = MagicMock(spec=DownloadHandlers)

        content = create_security_tab_content(download_handlers)
        layout = content.layout()

        # Find all child widgets
        cards = []
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                # Recursively find ModernCard widgets
                cards.extend(widget.findChildren(type(widget)))

        # Verify we have the security tool cards
        assert len(cards) > 0

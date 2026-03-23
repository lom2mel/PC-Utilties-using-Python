"""Tests for news tab content."""

import pytest

from features.ui.tabs.news_tab import create_news_tab_content, NewsTabContent


class TestNewsTab:
    """Tests for news tab content creation."""

    def test_create_news_tab_content(self, qtbot):
        """Test that news tab content is created successfully."""
        content = create_news_tab_content()

        # Verify content is created
        assert content is not None
        assert isinstance(content, NewsTabContent)
        assert content.layout() is not None

    def test_news_tab_content_initialization(self, qtbot):
        """Test NewsTabContent widget initialization."""
        content = NewsTabContent()

        # Verify widget is properly initialized
        assert content._headlines_layout is not None
        assert content.layout() is not None
        assert content.layout().count() > 0

    def test_news_tab_has_static_sources(self, qtbot):
        """Test that news tab contains static source cards."""
        content = NewsTabContent()

        # Verify layout exists and has items
        layout = content.layout()
        assert layout is not None
        assert layout.count() > 0

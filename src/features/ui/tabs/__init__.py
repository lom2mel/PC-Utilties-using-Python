"""Tab content modules for PC Utilities Manager.

This package provides tab content creators for the main application window.
Each tab is responsible for creating its own content widget.
"""

from features.ui.tabs.security_tab import create_security_tab_content
from features.ui.tabs.converters_tab import create_converters_tab_content
from features.ui.tabs.news_tab import create_news_tab_content, NewsTabContent
from features.ui.tabs.antivirus_deals_tab import (
    create_antivirus_deals_tab_content,
    AntivirusDealsTabContent,
)

__all__ = [
    "create_security_tab_content",
    "create_converters_tab_content",
    "create_news_tab_content",
    "create_antivirus_deals_tab_content",
    "NewsTabContent",
    "AntivirusDealsTabContent",
]

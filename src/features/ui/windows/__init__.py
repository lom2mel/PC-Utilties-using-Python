"""Window component modules for PC Utilities Manager.

This package provides reusable window components like menu bars,
headers, and status indicators for the main application window.
"""

from features.ui.windows.header import create_header
from features.ui.windows.main_menu import create_menu_bar, MenuCallbacks
from features.ui.windows.status_indicator import StatusIndicatorWidget

__all__ = [
    "create_header",
    "create_menu_bar",
    "MenuCallbacks",
    "StatusIndicatorWidget",
]

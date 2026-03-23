"""Modern redesigned UI for PC Utilities Manager with professional UX.

This module provides the main application window with a modern card-based interface
for accessing PC utilities and file converters. Uses tab-based navigation
for better UX and organization.

Refactored to use extracted tab and window component modules.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox,
    QScrollArea,
    QMainWindow,
    QFrame,
)
from PySide6.QtCore import Qt

from features.ui.components import ModernTabWidget
from features.ui.design_system import COLORS
from features.ui.download_handlers import DownloadHandlers
from features.ui.converter_handlers import ConverterHandlers
from features.ui.ui_config import CONFIG
from features.ui.state_manager import get_state_manager

# Import extracted components
from features.ui.tabs import (
    create_security_tab_content,
    create_converters_tab_content,
    create_news_tab_content,
)
from features.ui.windows import (
    create_header,
    create_menu_bar,
    MenuCallbacks,
    StatusIndicatorWidget,
)


class ModernDownloadManager(QMainWindow):
    """Modern redesigned PC Utilities Manager with professional UI/UX.

    Features:
    - Tab-based navigation for better organization
    - Card-based interface with hover effects
    - Security tools for downloading antivirus and scanners
    - File converters for Office documents and images
    - Menu bar with keyboard shortcuts
    - Status indicator for operation feedback

    Attributes:
        download_handlers: Handler for download operations
        converter_handlers: Handler for file conversion operations
        tab_widget: Tab widget for navigation
        state_manager: State manager for tracking application state
        status_indicator: Status indicator widget
    """

    def __init__(self):
        """Initialize the modern download manager window."""
        super().__init__()
        self.state_manager = get_state_manager()

        # Initialize handlers
        self.download_handlers = DownloadHandlers()
        self.converter_handlers = ConverterHandlers()

        # Initialize UI
        self.init_ui()

        # Connect handler signals to status indicator
        self.download_handlers.status_changed.connect(
            lambda msg, success: self.status_indicator.update_status(msg, success)
        )
        self.converter_handlers.status_changed.connect(
            lambda msg, success: self.status_indicator.update_status(msg, success)
        )

    def init_ui(self) -> None:
        """Initialize modern UI with tab-based card layout."""
        self.setWindowTitle("PC Utilities Manager")
        self.setMinimumSize(900, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)

        # Create menu bar with callbacks
        callbacks = MenuCallbacks(
            on_office_converter=self._on_office_converter,
            on_picture_to_pdf=self._on_picture_to_pdf,
            on_exit=self.close,
            on_about=self.show_about,
        )
        create_menu_bar(self.menuBar(), callbacks)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout with scroll area
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header section
        header = create_header(on_about_clicked=self.show_about)
        main_layout.addWidget(header)

        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Status indicator
        self.status_indicator = StatusIndicatorWidget()
        content_layout.addWidget(self.status_indicator)

        # Create tab widget with frozen configuration
        tabs = CONFIG.tabs.get_all_tabs()
        self.tab_widget = ModernTabWidget(
            tabs=tabs,
            active_tab_id=self.state_manager.get_active_tab_id()
        )
        self.tab_widget.tab_changed.connect(self._on_tab_changed)
        content_layout.addWidget(self.tab_widget)

        # Create and add tab content
        security_content = create_security_tab_content(self.download_handlers)
        converters_content = create_converters_tab_content(
            self.converter_handlers,
            self.start_conversion,
            self.start_picture_to_pdf_conversion,
        )
        news_content = create_news_tab_content()

        # Map tab IDs - need to match CONFIG.tabs IDs
        self.tab_widget.add_tab_content("security", security_content)
        self.tab_widget.add_tab_content("converters", converters_content)
        # Note: news tab uses "cyber_security_news" in CONFIG
        self.tab_widget.add_tab_content("cyber_security_news", news_content)

        content_layout.addStretch()

        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        central_widget.setLayout(main_layout)

    def _on_tab_changed(self, tab_id: str) -> None:
        """Handle tab change event.

        Args:
            tab_id: ID of the newly active tab
        """
        self.state_manager.switch_tab(tab_id)

    def _on_office_converter(self) -> None:
        """Handle Office Converter menu action."""
        self.converter_handlers.open_converter_dialog(
            self,
            {
                'file': lambda: self.converter_handlers.select_file_to_convert(
                    self, self.start_conversion
                ),
                'folder': lambda: self.converter_handlers.select_folder_to_convert(
                    self, self.start_conversion
                ),
                'drive': lambda: self.converter_handlers.select_drive_to_convert(
                    self, self.start_conversion
                ),
            }
        )

    def _on_picture_to_pdf(self) -> None:
        """Handle Picture to PDF menu action."""
        self.converter_handlers.open_picture_to_pdf_dialog(
            self, self.start_picture_to_pdf_conversion
        )

    def start_conversion(self, path: str, is_file: bool = False) -> None:
        """Start Office file conversion process.

        Args:
            path: File or folder path to convert
            is_file: True if path is a single file, False for folder/drive
        """
        self.converter_handlers.start_conversion(self, path, is_file)

    def start_picture_to_pdf_conversion(self, image_files: list, output_path: str) -> None:
        """Start image to PDF conversion process.

        Args:
            image_files: List of image file paths to convert
            output_path: Output PDF file path
        """
        self.converter_handlers.start_picture_to_pdf_conversion(self, image_files, output_path)

    def show_about(self) -> None:
        """Show About dialog with application information."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("About PC Utilities Manager")
        msg.setText("PC Utilities Manager")
        msg.setInformativeText(
            "Version 2.0 - Modern UI\n\n"
            "A modern utility application for managing PC maintenance tools "
            "and converting files to the latest formats.\n\n"
            "Created by: Lomel A. Arguelles\n"
            "© 2025\n\n"
            "---\n\n"
            "This application uses PySide6 (Qt for Python),\n"
            "licensed under the GNU Lesser General Public License v3.0.\n\n"
            "PySide6 Repository:\n"
            "https://code.qt.io/cgit/pyside/pyside-setup.git/\n\n"
            "For license details, see LICENSE.txt included with this application."
        )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

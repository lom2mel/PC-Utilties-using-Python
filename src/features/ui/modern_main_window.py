"""Modern redesigned UI for PC Utilities Manager with professional UX.

This module provides the main application window with a modern card-based interface
for accessing PC utilities and file converters. Now with tab-based navigation
for better UX and organization.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QMessageBox,
    QScrollArea,
    QMenuBar,
    QMainWindow,
    QFrame,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QAction, QKeySequence

from features.ui.components import ModernCard, SectionHeader, ModernTabWidget
from features.ui.download_handlers import DownloadHandlers
from features.ui.converter_handlers import ConverterHandlers
from features.ui.ui_config import CONFIG
from features.ui.state_manager import get_state_manager


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
    """

    def __init__(self):
        """Initialize the modern download manager window."""
        super().__init__()
        self.state_manager = get_state_manager()
        self.init_ui()

        # Initialize handlers
        self.download_handlers = DownloadHandlers()
        self.converter_handlers = ConverterHandlers()

        # Connect handler signals
        self.download_handlers.status_changed.connect(self.update_status)
        self.converter_handlers.status_changed.connect(self.update_status)

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

        # Create menu bar
        self.create_menu_bar()

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout with scroll area
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header section
        header = self.create_header()
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
        self.status_indicator = self.create_status_indicator()
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
        security_content = self.create_security_tab_content()
        converters_content = self.create_converters_tab_content()

        self.tab_widget.add_tab_content("security", security_content)
        self.tab_widget.add_tab_content("converters", converters_content)

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

    def create_menu_bar(self) -> None:
        """Create menu bar with File and Help menus."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        # Office Converter action
        converter_action = QAction("&Office File Converter", self)
        converter_action.setShortcut(QKeySequence("Ctrl+O"))
        converter_action.setStatusTip("Convert Office files to latest format")
        converter_action.triggered.connect(
            lambda: self.converter_handlers.open_converter_dialog(
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
        )
        file_menu.addAction(converter_action)

        # Picture to PDF action
        pdf_action = QAction("&Picture to PDF", self)
        pdf_action.setShortcut(QKeySequence("Ctrl+P"))
        pdf_action.setStatusTip("Convert images to PDF")
        pdf_action.triggered.connect(
            lambda: self.converter_handlers.open_picture_to_pdf_dialog(
                self, self.start_picture_to_pdf_conversion
            )
        )
        file_menu.addAction(pdf_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        # About action
        about_action = QAction("&About", self)
        about_action.setShortcut(QKeySequence("F1"))
        about_action.setStatusTip("About this application")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_header(self) -> QWidget:
        """Create modern header with branding.

        Returns:
            Header widget with gradient background
        """
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667EEA, stop:1 #764BA2
                );
                border-bottom: 3px solid rgba(255, 255, 255, 0.2);
            }
        """)
        header.setFixedHeight(120)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)

        # Title
        title = QLabel("🛠️ PC Utilities Manager")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel(
            "Essential tools for system maintenance, security, and file management"
        )
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: "
                              "transparent;")
        layout.addWidget(subtitle)

        # About button
        about_btn = QPushButton("About")
        about_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        about_btn.clicked.connect(self.show_about)
        about_btn.setMinimumWidth(80)
        about_btn.setMinimumHeight(36)
        layout.addWidget(about_btn, alignment=Qt.AlignRight | Qt.AlignTop)

        header.setLayout(layout)
        return header

    def create_status_indicator(self) -> QWidget:
        """Create modern status indicator.

        Returns:
            Status widget with icon and message label
        """
        status_widget = QWidget()
        status_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)

        # Status icon
        self.status_icon = QLabel("✓")
        self.status_icon.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.status_icon.setStyleSheet("color: #4CAF50; background: transparent;")

        # Status text
        self.status_label = QLabel("Ready to use")
        self.status_label.setFont(QFont("Segoe UI", 11))
        self.status_label.setStyleSheet("color: #1F1F1F; background: transparent;")

        layout.addWidget(self.status_icon)
        layout.addWidget(self.status_label)

        status_widget.setLayout(layout)
        return status_widget

    def create_security_tab_content(self) -> QWidget:
        """Create security tools tab content with cards.

        Returns:
            Widget with security tool cards for the security tab
        """
        from PySide6.QtWidgets import QWidget

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Section header
        header = SectionHeader(
            "🔒 Security & Maintenance Tools",
            "Download and use essential security utilities to keep your PC safe"
        )
        layout.addWidget(header)

        # Cards grid
        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)

        # Avast card
        avast_card = ModernCard(
            "Avast Antivirus",
            "Download free antivirus protection for your PC",
            "🛡️",
            "#FF6600"
        )
        avast_card.mousePressEvent = lambda e: self.download_handlers.download_avast()
        cards_layout.addWidget(avast_card, 0, 0)

        # VirusTotal card
        virustotal_card = ModernCard(
            "VirusTotal Scanner",
            "Scan files for viruses and malware online",
            "🔍",
            "#394EFF"
        )
        virustotal_card.mousePressEvent = lambda e: self.download_handlers.open_virustotal()
        cards_layout.addWidget(virustotal_card, 0, 1)

        # CCleaner card
        ccleaner_card = ModernCard(
            "CCleaner",
            "Clean and optimize your PC performance",
            "🧹",
            "#0066CC"
        )
        ccleaner_card.mousePressEvent = lambda e: self.download_handlers.download_ccleaner()
        cards_layout.addWidget(ccleaner_card, 0, 2)

        # Speccy card
        speccy_card = ModernCard(
            "Speccy",
            "View detailed system information and specifications",
            "💻",
            "#00A4EF"
        )
        speccy_card.mousePressEvent = lambda e: self.download_handlers.download_speccy()
        cards_layout.addWidget(speccy_card, 1, 0)

        layout.addLayout(cards_layout)
        layout.addStretch()
        content.setLayout(layout)
        return content

    def create_converters_tab_content(self) -> QWidget:
        """Create file converters tab content with cards.

        Returns:
            Widget with file converter cards for the converters tab
        """
        from PySide6.QtWidgets import QWidget

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Section header
        header = SectionHeader(
            "📁 File Converters",
            "Convert your documents and images to modern formats"
        )
        layout.addWidget(header)

        # Cards grid
        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)

        # Office converter card
        office_card = ModernCard(
            "Office File Converter",
            "Convert old Office files to latest format (.docx, .xlsx, .pptx)",
            "📄",
            "#217346"
        )
        office_card.mousePressEvent = lambda e: self.converter_handlers.open_converter_dialog(
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
        cards_layout.addWidget(office_card, 0, 0)

        # Picture to PDF card
        pdf_card = ModernCard(
            "Picture to PDF",
            "Convert images to PDF documents quickly and easily",
            "🖼️",
            "#D83B01"
        )
        pdf_card.mousePressEvent = lambda e: self.converter_handlers.open_picture_to_pdf_dialog(
            self, self.start_picture_to_pdf_conversion
        )
        cards_layout.addWidget(pdf_card, 0, 1)

        # Placeholder for future feature
        placeholder_card = QFrame()
        placeholder_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px dashed #E0E0E0;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        placeholder_layout = QVBoxLayout()
        placeholder_text = QLabel("More tools\ncoming soon...")
        placeholder_text.setFont(QFont("Segoe UI", 11))
        placeholder_text.setStyleSheet("color: #999999;")
        placeholder_text.setAlignment(Qt.AlignCenter)
        placeholder_layout.addWidget(placeholder_text)
        placeholder_card.setLayout(placeholder_layout)
        cards_layout.addWidget(placeholder_card, 0, 2)

        layout.addLayout(cards_layout)
        layout.addStretch()
        content.setLayout(layout)
        return content

    def update_status(self, message: str, success: bool = True) -> None:
        """Update status indicator with message.

        Args:
            message: Status message to display
            success: True for success (green), False for warning (orange)
        """
        icon = "✓" if success else "⚠"
        color = "#4CAF50" if success else "#FF9800"

        self.status_icon.setText(icon)
        self.status_icon.setStyleSheet(f"color: {color}; background: transparent;")
        self.status_label.setText(message)

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

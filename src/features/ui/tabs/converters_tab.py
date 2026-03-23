"""File converters tab content for PC Utilities Manager.

This module provides the file converters tab with cards for
converting Office documents and images to PDF.
"""

from typing import Callable
from PySide6.QtWidgets import QWidget, QGridLayout, QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from features.ui.components import ModernCard, SectionHeader
from features.ui.design_system import COLORS, SPACING


def create_converters_tab_content(
    converter_handlers: "ConverterHandlers",
    start_conversion_callback: Callable[[str, bool], None],
    start_picture_to_pdf_callback: Callable[[list, str], None],
) -> QWidget:
    """Create file converters tab content with cards.

    Args:
        converter_handlers: Handler for file conversion operations
        start_conversion_callback: Function to start Office file conversion
        start_picture_to_pdf_callback: Function to start image to PDF conversion

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
    office_card.mousePressEvent = lambda e: converter_handlers.open_converter_dialog(
        None,  # Parent will be set by main window
        {
            'file': lambda: converter_handlers.select_file_to_convert(
                None, start_conversion_callback
            ),
            'folder': lambda: converter_handlers.select_folder_to_convert(
                None, start_conversion_callback
            ),
            'drive': lambda: converter_handlers.select_drive_to_convert(
                None, start_conversion_callback
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
    pdf_card.mousePressEvent = lambda e: converter_handlers.open_picture_to_pdf_dialog(
        None, start_picture_to_pdf_callback
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

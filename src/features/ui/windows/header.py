"""Header component for PC Utilities Manager.

This module provides the modern gradient header with branding
and about button for the main application window.
"""

from typing import Callable, Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


def create_header(
    title: str = "🛠️ PC Utilities Manager",
    subtitle: str = "Essential tools for system maintenance, security, and file management",
    on_about_clicked: Optional[Callable[[], None]] = None,
) -> QWidget:
    """Create modern header with branding.

    Args:
        title: Header title text
        subtitle: Header subtitle text
        on_about_clicked: Optional callback for about button click

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
    title_label = QLabel(title)
    title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
    title_label.setStyleSheet("color: white; background: transparent;")
    layout.addWidget(title_label)

    # Subtitle
    subtitle_label = QLabel(subtitle)
    subtitle_label.setFont(QFont("Segoe UI", 11))
    subtitle_label.setStyleSheet(
        "color: rgba(255, 255, 255, 0.9); background: transparent;"
    )
    layout.addWidget(subtitle_label)

    # About button (if callback provided)
    if on_about_clicked is not None:
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
        about_btn.clicked.connect(on_about_clicked)
        about_btn.setMinimumWidth(80)
        about_btn.setMinimumHeight(36)
        layout.addWidget(about_btn, alignment=Qt.AlignRight | Qt.AlignTop)

    header.setLayout(layout)
    return header

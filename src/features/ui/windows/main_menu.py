"""Menu bar component for PC Utilities Manager.

This module provides the menu bar with File and Help menus
for the main application window.
"""

from dataclasses import dataclass
from typing import Callable, Optional
from PySide6.QtWidgets import QMenuBar
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtCore import QObject


@dataclass(frozen=True)
class MenuCallbacks:
    """Frozen dataclass for menu action callbacks.

    Attributes:
        on_office_converter: Callback for Office file converter action
        on_picture_to_pdf: Callback for Picture to PDF action
        on_exit: Callback for Exit action
        on_about: Callback for About action
    """

    on_office_converter: Optional[Callable[[], None]] = None
    on_picture_to_pdf: Optional[Callable[[], None]] = None
    on_exit: Optional[Callable[[], None]] = None
    on_about: Optional[Callable[[], None]] = None


def create_menu_bar(
    menubar: QMenuBar,
    callbacks: MenuCallbacks,
) -> None:
    """Create menu bar with File and Help menus.

    Args:
        menubar: The menu bar to populate
        callbacks: Frozen dataclass containing menu action callbacks
    """
    # File menu
    file_menu = menubar.addMenu("&File")

    # Office Converter action
    if callbacks.on_office_converter is not None:
        converter_action = QAction("&Office File Converter", menubar.parent())
        converter_action.setShortcut(QKeySequence("Ctrl+O"))
        converter_action.setStatusTip("Convert Office files to latest format")
        converter_action.triggered.connect(callbacks.on_office_converter)
        file_menu.addAction(converter_action)

    # Picture to PDF action
    if callbacks.on_picture_to_pdf is not None:
        pdf_action = QAction("&Picture to PDF", menubar.parent())
        pdf_action.setShortcut(QKeySequence("Ctrl+P"))
        pdf_action.setStatusTip("Convert images to PDF")
        pdf_action.triggered.connect(callbacks.on_picture_to_pdf)
        file_menu.addAction(pdf_action)

    if callbacks.on_office_converter is not None or callbacks.on_picture_to_pdf is not None:
        file_menu.addSeparator()

    # Exit action
    if callbacks.on_exit is not None:
        exit_action = QAction("E&xit", menubar.parent())
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(callbacks.on_exit)
        file_menu.addAction(exit_action)

    # Help menu
    help_menu = menubar.addMenu("&Help")

    # About action
    if callbacks.on_about is not None:
        about_action = QAction("&About", menubar.parent())
        about_action.setShortcut(QKeySequence("F1"))
        about_action.setStatusTip("About this application")
        about_action.triggered.connect(callbacks.on_about)
        help_menu.addAction(about_action)

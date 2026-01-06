"""Tests for ModernDownloadManager and related components."""

from pytestqt.qtbot import QtBot
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QMessageBox

from features.ui.modern_main_window import ModernDownloadManager
from features.ui.components import ModernCard, SectionHeader
from features.ui.download_handlers import DownloadHandlers
from features.ui.converter_handlers import ConverterHandlers


def test_download_manager_instantiation(qtbot: QtBot):
    """Test that ModernDownloadManager can be instantiated."""
    widget = ModernDownloadManager()
    qtbot.addWidget(widget)
    assert widget is not None
    assert widget.windowTitle() == "PC Utilities Manager"
    assert widget.minimumWidth() == 900
    assert widget.minimumHeight() == 700


def test_download_handlers_initialization(qtbot: QtBot):
    """Test that download handlers are properly initialized."""
    widget = ModernDownloadManager()
    qtbot.addWidget(widget)

    assert widget.download_handlers is not None
    assert isinstance(widget.download_handlers, DownloadHandlers)
    assert widget.converter_handlers is not None
    assert isinstance(widget.converter_handlers, ConverterHandlers)


def test_show_about(qtbot: QtBot):
    """Test that show_about method displays the about dialog."""
    widget = ModernDownloadManager()
    qtbot.addWidget(widget)

    with patch.object(QMessageBox, 'exec') as mock_exec:
        widget.show_about()
        # Verify the dialog would have been shown
        assert mock_exec.called


def test_status_update(qtbot: QtBot):
    """Test that status indicator can be updated."""
    widget = ModernDownloadManager()
    qtbot.addWidget(widget)

    # Test success status
    widget.update_status("Test message", success=True)
    assert widget.status_label.text() == "Test message"
    assert widget.status_icon.text() == "✓"

    # Test error status
    widget.update_status("Error message", success=False)
    assert widget.status_label.text() == "Error message"
    assert widget.status_icon.text() == "⚠"


def test_components_instantiation(qtbot: QtBot):
    """Test that UI components can be instantiated."""
    card = ModernCard(
        title="Test Card",
        description="Test description",
        icon_text="🧪",
        color="#FF0000"
    )
    qtbot.addWidget(card)
    assert card is not None

    header = SectionHeader(
        title="Test Section",
        description="Test description"
    )
    qtbot.addWidget(header)
    assert header is not None


def test_download_handlers_signals(qtbot: QtBot):
    """Test that download handlers emit status signals."""
    handler = DownloadHandlers()
    status_messages = []

    def capture_status(message: str, success: bool):
        status_messages.append((message, success))

    handler.status_changed.connect(capture_status)

    with patch('webbrowser.open'):
        handler.download_avast()

    assert len(status_messages) > 0
    assert any("Avast" in msg for msg, _ in status_messages)


def test_converter_handlers_office_check(qtbot: QtBot):
    """Test that converter handlers can check for Office installation."""
    handler = ConverterHandlers()
    # This will return False if Office is not installed
    result = handler.check_office_installed()
    assert isinstance(result, bool)


def test_menu_bar_creation(qtbot: QtBot):
    """Test that menu bar is created with all expected menus."""
    widget = ModernDownloadManager()
    qtbot.addWidget(widget)

    menubar = widget.menuBar()
    assert menubar is not None

    # Check for File and Help menus
    actions = menubar.actions()
    menu_texts = [action.text() for action in actions]
    assert "File" in menu_texts
    assert "Help" in menu_texts


def test_security_section_creation(qtbot: QtBot):
    """Test that security section is created with all cards."""
    widget = ModernDownloadManager()
    qtbot.addWidget(widget)

    security_section = widget.create_security_section()
    assert security_section is not None
    assert security_section.layout() is not None


def test_converters_section_creation(qtbot: QtBot):
    """Test that converters section is created with all cards."""
    widget = ModernDownloadManager()
    qtbot.addWidget(widget)

    converters_section = widget.create_converters_section()
    assert converters_section is not None
    assert converters_section.layout() is not None


def test_header_creation(qtbot: QtBot):
    """Test that header widget is created properly."""
    widget = ModernDownloadManager()
    qtbot.addWidget(widget)

    header = widget.create_header()
    assert header is not None
    assert header.height() == 120
    assert header.layout() is not None


def test_status_indicator_creation(qtbot: QtBot):
    """Test that status indicator is created with default values."""
    widget = ModernDownloadManager()
    qtbot.addWidget(widget)

    status_widget = widget.create_status_indicator()
    assert status_widget is not None
    assert widget.status_label.text() == "Ready to use"
    assert widget.status_icon.text() == "✓"

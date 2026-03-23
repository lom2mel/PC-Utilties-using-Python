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
    widget.status_indicator.update_status("Test message", success=True)
    assert widget.status_indicator.message == "Test message"
    assert widget.status_indicator.success is True

    # Test error status
    widget.status_indicator.update_status("Error message", success=False)
    assert widget.status_indicator.message == "Error message"
    assert widget.status_indicator.success is False


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

    # Check for File and Help menus (with mnemonics)
    actions = menubar.actions()
    menu_texts = [action.text() for action in actions]
    assert "&File" in menu_texts
    assert "&Help" in menu_texts


def test_status_indicator_exists(qtbot: QtBot):
    """Test that status indicator widget is created."""
    widget = ModernDownloadManager()
    qtbot.addWidget(widget)

    assert widget.status_indicator is not None
    assert widget.status_indicator.message == "Ready to use"


def test_tab_widget_exists(qtbot: QtBot):
    """Test that tab widget is created."""
    widget = ModernDownloadManager()
    qtbot.addWidget(widget)

    assert widget.tab_widget is not None

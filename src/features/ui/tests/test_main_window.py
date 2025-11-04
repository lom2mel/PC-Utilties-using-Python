from pytestqt.qtbot import QtBot
from unittest.mock import patch
from features.ui.main_window import DownloadManager


def test_download_manager_instantiation(qtbot: QtBot):
    """Test that DownloadManager can be instantiated."""
    # QApplication instance is automatically created by pytest-qt
    widget = DownloadManager()
    qtbot.addWidget(widget)
    assert widget is not None


@patch("features.ui.main_window.QMessageBox")
def test_show_about(mock_qmessagebox, qtbot: QtBot):
    """Test that show_about method shows a message box."""
    widget = DownloadManager()
    qtbot.addWidget(widget)

    widget.show_about()

    mock_qmessagebox.assert_called_once()
    # Further assertions can be made on the mock_qmessagebox instance
    # to check the title, text, etc. of the message box.

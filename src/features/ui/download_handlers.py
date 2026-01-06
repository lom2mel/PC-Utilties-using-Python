"""Download handlers for PC utilities.

This module contains handlers for opening external download pages for various
PC utilities and security tools.
"""

import webbrowser
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject, Signal


class DownloadHandlers(QObject):
    """Handlers for download-related actions.

    Manages opening external URLs for downloading PC utilities like
    antivirus software, system cleaners, and scanning tools.

    Signals:
        status_changed: Emitted when download status changes (message, success)
    """

    status_changed = Signal(str, bool)

    # Download URLs as class constants
    AVAST_URL = (
        "https://www.avast.com/download-thank-you.php?product=AV-FREE-ONLINE"
        "&loc=en-us"
    )
    VIRUSTOTAL_URL = "https://www.virustotal.com/gui/home/upload"
    CCLEANER_URL = "https://www.ccleaner.com/ccleaner/download/standard"
    SPECCY_URL = "https://www.ccleaner.com/speccy/download/standard"

    def download_avast(self) -> None:
        """Open Avast Antivirus download page in browser.

        Updates status and shows confirmation message when successful.
        """
        self.status_changed.emit("Opening Avast download page...", True)
        try:
            webbrowser.open(self.AVAST_URL)
            self.status_changed.emit("Avast download page opened in browser", True)
            self._show_download_message("Avast Antivirus")
        except Exception as e:
            self.status_changed.emit(f"Error: {str(e)}", False)

    def download_ccleaner(self) -> None:
        """Open CCleaner download page in browser.

        Updates status and shows confirmation message when successful.
        """
        self.status_changed.emit("Opening CCleaner download page...", True)
        try:
            webbrowser.open(self.CCLEANER_URL)
            self.status_changed.emit("CCleaner download page opened in browser", True)
            self._show_download_message("CCleaner")
        except Exception as e:
            self.status_changed.emit(f"Error: {str(e)}", False)

    def download_speccy(self) -> None:
        """Open Speccy download page in browser.

        Updates status and shows confirmation message when successful.
        """
        self.status_changed.emit("Opening Speccy download page...", True)
        try:
            webbrowser.open(self.SPECCY_URL)
            self.status_changed.emit("Speccy download page opened in browser", True)
            self._show_download_message("Speccy")
        except Exception as e:
            self.status_changed.emit(f"Error: {str(e)}", False)

    def open_virustotal(self) -> None:
        """Open VirusTotal scanner in browser.

        Shows information message about using VirusTotal for file scanning.
        """
        self.status_changed.emit("Opening VirusTotal...", True)
        try:
            webbrowser.open(self.VIRUSTOTAL_URL)
            self.status_changed.emit("VirusTotal opened in browser", True)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("VirusTotal Opened")
            msg.setText("VirusTotal file scanner opened!")
            msg.setInformativeText(
                "You can now upload any file to scan it for viruses and malware."
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        except Exception as e:
            self.status_changed.emit(f"Error: {str(e)}", False)

    def _show_download_message(self, app_name: str) -> None:
        """Show download confirmation message.

        Args:
            app_name: Name of the application being downloaded
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Download Started")
        msg.setText(f"{app_name} download page opened!")
        msg.setInformativeText(
            f"The {app_name} download should start automatically in your browser.\n"
            "The file will be saved to your Downloads folder."
        )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

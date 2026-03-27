"""Download handlers for PC utilities.

This module contains handlers for opening external download pages for various
PC utilities and security tools.
"""

import webbrowser
from PySide6.QtCore import QObject, Signal


class DownloadHandlers(QObject):
    """Handlers for download-related actions.

    Manages opening external URLs for downloading PC utilities like
    antivirus software, system cleaners, and scanning tools.

    Signals:
        status_changed: Emitted when download status changes (message, success)
    """

    status_changed = Signal(str, bool)

    # Download URLs as class constants (product pages, not direct downloads)
    AVAST_URL = "https://www.avast.com/free-antivirus-download"
    VIRUSTOTAL_URL = "https://www.virustotal.com/gui/home/upload"
    CCLEANER_URL = "https://www.ccleaner.com/ccleaner"
    SPECCY_URL = "https://www.ccleaner.com/speccy"
    BITDEFENDER_URL = "https://www.bitdefender.com/en-us/consumer/free-antivirus"

    def download_avast(self) -> None:
        """Open Avast Antivirus product page in browser.

        Updates status when successful.
        """
        self.status_changed.emit("Opening Avast product page...", True)
        try:
            webbrowser.open(self.AVAST_URL)
            self.status_changed.emit("Avast product page opened in browser", True)
        except Exception as e:
            self.status_changed.emit(f"Error: {str(e)}", False)

    def download_ccleaner(self) -> None:
        """Open CCleaner product page in browser.

        Updates status when successful.
        """
        self.status_changed.emit("Opening CCleaner product page...", True)
        try:
            webbrowser.open(self.CCLEANER_URL)
            self.status_changed.emit("CCleaner product page opened in browser", True)
        except Exception as e:
            self.status_changed.emit(f"Error: {str(e)}", False)

    def download_speccy(self) -> None:
        """Open Speccy product page in browser.

        Updates status when successful.
        """
        self.status_changed.emit("Opening Speccy product page...", True)
        try:
            webbrowser.open(self.SPECCY_URL)
            self.status_changed.emit("Speccy product page opened in browser", True)
        except Exception as e:
            self.status_changed.emit(f"Error: {str(e)}", False)

    def open_virustotal(self) -> None:
        """Open VirusTotal scanner in browser.

        Updates status when successful.
        """
        self.status_changed.emit("Opening VirusTotal...", True)
        try:
            webbrowser.open(self.VIRUSTOTAL_URL)
            self.status_changed.emit("VirusTotal opened in browser", True)
        except Exception as e:
            self.status_changed.emit(f"Error: {str(e)}", False)

    def download_bitdefender(self) -> None:
        """Open Bitdefender Antivirus product page in browser.

        Updates status when successful.
        """
        self.status_changed.emit("Opening Bitdefender product page...", True)
        try:
            webbrowser.open(self.BITDEFENDER_URL)
            self.status_changed.emit("Bitdefender product page opened in browser", True)
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

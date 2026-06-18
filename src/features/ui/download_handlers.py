"""Download handlers for PC utilities.

This module contains handlers for opening external download pages for various
PC utilities and security tools.
"""

import logging
import webbrowser
from PySide6.QtCore import QObject, Signal

from features.ui.exceptions import DownloadHandlerError, NetworkError

logger = logging.getLogger(__name__)


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
        """Open Avast Antivirus product page in browser."""
        self._open_tool_page("Avast", self.AVAST_URL)

    def download_ccleaner(self) -> None:
        """Open CCleaner product page in browser."""
        self._open_tool_page("CCleaner", self.CCLEANER_URL)

    def download_speccy(self) -> None:
        """Open Speccy product page in browser."""
        self._open_tool_page("Speccy", self.SPECCY_URL)

    def open_virustotal(self) -> None:
        """Open VirusTotal scanner in browser."""
        self._open_tool_page("VirusTotal", self.VIRUSTOTAL_URL, action="scanner")

    def download_bitdefender(self) -> None:
        """Open Bitdefender Antivirus product page in browser."""
        self._open_tool_page("Bitdefender", self.BITDEFENDER_URL)

    def _open_tool_page(self, app_name: str, url: str, action: str = "product page") -> None:
        """Generic handler for opening security tool download pages.

        Args:
            app_name: Name of the application/tool
            url: URL to open in browser
            action: Type of page (default: "product page")

        Raises:
            NetworkError: If webbrowser fails to open the URL
        """
        self.status_changed.emit(f"Opening {app_name} {action}...", True)
        try:
            webbrowser.open(url)
            self.status_changed.emit(f"{app_name} {action} opened in browser", True)
            logger.info(f"Successfully opened {app_name} {action}: {url}")
        except Exception as e:
            error_msg = f"Error opening {app_name}: {str(e)}"
            self.status_changed.emit(error_msg, False)
            logger.error(f"{error_msg} - URL: {url}")

            # Re-raise as specific exception for external handling
            raise NetworkError(
                f"Failed to open {app_name} {action}",
                url=url,
                original_error=e
            ) from e

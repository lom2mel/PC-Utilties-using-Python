"""Main entry point for PC Utilities Manager.

Run this script to launch the PC Utilities Manager application.
"""

import sys
from pathlib import Path

# Add src directory to Python path for imports
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from PySide6.QtWidgets import QApplication
from features.ui.modern_main_window import ModernDownloadManager


def main() -> None:
    """Launch the PC Utilities Manager application."""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("PC Utilities Manager")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("PC Utilities")

    window = ModernDownloadManager()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

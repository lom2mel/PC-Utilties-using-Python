import sys
from PySide6.QtWidgets import QApplication
from features.ui.main_window import DownloadManager

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("PC Utilities Download Manager")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("PC Utilities")
    
    window = DownloadManager()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

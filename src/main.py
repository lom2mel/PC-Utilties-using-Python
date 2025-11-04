import sys
from PySide6.QtWidgets import QApplication
from features.ui.modern_main_window import ModernDownloadManager

def main():
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

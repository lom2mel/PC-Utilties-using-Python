import sys
import os
import webbrowser
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class DownloadManager(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Download URLs (official download links)
        self.avast_url = "https://www.avast.com/download-thank-you.php?product=AV-FREE-ONLINE&loc=en-us"
        self.ccleaner_url = "https://www.ccleaner.com/ccleaner/download/standard"
        
    def init_ui(self):
        self.setWindowTitle("PC Utilities Download Manager")
        self.setGeometry(300, 300, 400, 250)
        self.setFixedSize(400, 250)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("PC Utilities Download Manager")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # Status label
        self.status_label = QLabel("Ready to download")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Download Avast Button
        self.avast_button = QPushButton("Download Avast Antivirus")
        self.avast_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6600;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E55A00;
            }
            QPushButton:pressed {
                background-color: #CC5200;
            }
        """)
        self.avast_button.clicked.connect(self.download_avast)
        layout.addWidget(self.avast_button)
        
        # Download CCleaner Button
        self.ccleaner_button = QPushButton("Download CCleaner")
        self.ccleaner_button.setStyleSheet("""
            QPushButton {
                background-color: #0066CC;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0052A3;
            }
            QPushButton:pressed {
                background-color: #003D7A;
            }
        """)
        self.ccleaner_button.clicked.connect(self.download_ccleaner)
        layout.addWidget(self.ccleaner_button)
        
        # Info label
        info_label = QLabel("Files will be downloaded to your Downloads folder")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(info_label)
        
        self.setLayout(layout)
        
    def download_avast(self):
        """Download Avast Antivirus by opening the official download page"""
        self.status_label.setText("Opening Avast download page...")
        try:
            webbrowser.open(self.avast_url)
            self.status_label.setText("Avast download page opened in browser")
            self.show_download_message("Avast Antivirus")
        except Exception as e:
            self.status_label.setText(f"Error opening Avast page: {str(e)}")
        
    def download_ccleaner(self):
        """Download CCleaner by opening the official download page"""
        self.status_label.setText("Opening CCleaner download page...")
        try:
            webbrowser.open(self.ccleaner_url)
            self.status_label.setText("CCleaner download page opened in browser")
            self.show_download_message("CCleaner")
        except Exception as e:
            self.status_label.setText(f"Error opening CCleaner page: {str(e)}")
    
    def show_download_message(self, app_name):
        """Show information message about the download"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Download Started")
        msg.setText(f"{app_name} download page opened!")
        msg.setInformativeText(f"The {app_name} download should start automatically in your browser.\nThe file will be saved to your Downloads folder.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()


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
    
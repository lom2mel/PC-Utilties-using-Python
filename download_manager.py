import sys
import os
import webbrowser
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                                QLabel, QMessageBox, QFileDialog, QProgressDialog)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from docx import Document
from openpyxl import load_workbook, Workbook
from pptx import Presentation
import shutil


class ConversionWorker(QThread):
    """Worker thread for converting Office files"""
    progress = Signal(int, int, str)  # current, total, current_file
    finished = Signal(dict)  # results dictionary

    def __init__(self, path, is_file=False):
        super().__init__()
        self.path = path
        self.is_file = is_file
        self.cancelled = False

    def run(self):
        """Execute the conversion process"""
        results = {
            'converted': 0,
            'skipped': 0,
            'errors': 0,
            'error_details': []
        }

        if self.is_file:
            files_to_convert = [Path(self.path)]
        else:
            files_to_convert = self.find_office_files(Path(self.path))

        total_files = len(files_to_convert)

        for idx, file_path in enumerate(files_to_convert):
            if self.cancelled:
                break

            self.progress.emit(idx + 1, total_files, str(file_path))

            try:
                if self.convert_file(file_path):
                    results['converted'] += 1
                else:
                    results['skipped'] += 1
            except Exception as e:
                results['errors'] += 1
                results['error_details'].append(f"{file_path.name}: {str(e)}")

        self.finished.emit(results)

    def find_office_files(self, root_path):
        """Recursively find all Office files in the given path"""
        office_extensions = {'.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'}
        office_files = []

        try:
            if root_path.is_file():
                if root_path.suffix.lower() in office_extensions:
                    office_files.append(root_path)
            else:
                for file_path in root_path.rglob('*'):
                    if file_path.is_file() and file_path.suffix.lower() in office_extensions:
                        # Skip backup files
                        if not file_path.name.endswith('.backup'):
                            office_files.append(file_path)
        except PermissionError as e:
            pass  # Skip directories we can't access

        return office_files

    def convert_file(self, file_path):
        """Convert a single Office file to the latest format"""
        extension = file_path.suffix.lower()

        # Create backup
        backup_path = file_path.with_suffix(file_path.suffix + '.backup')

        try:
            # Word documents
            if extension in ['.doc', '.docx']:
                doc = Document(str(file_path))

                # Create backup before conversion
                shutil.copy2(file_path, backup_path)

                # Save as .docx (latest format)
                new_path = file_path.with_suffix('.docx')
                doc.save(str(new_path))

                # If original was .doc, we can optionally remove it
                if extension == '.doc' and new_path != file_path:
                    pass  # Keep both files

                return True

            # Excel spreadsheets
            elif extension in ['.xls', '.xlsx']:
                wb = load_workbook(str(file_path))

                # Create backup before conversion
                shutil.copy2(file_path, backup_path)

                # Save as .xlsx (latest format)
                new_path = file_path.with_suffix('.xlsx')
                wb.save(str(new_path))

                return True

            # PowerPoint presentations
            elif extension in ['.ppt', '.pptx']:
                prs = Presentation(str(file_path))

                # Create backup before conversion
                shutil.copy2(file_path, backup_path)

                # Save as .pptx (latest format)
                new_path = file_path.with_suffix('.pptx')
                prs.save(str(new_path))

                return True

            return False

        except Exception as e:
            # If backup was created but conversion failed, we might want to restore
            if backup_path.exists():
                # Keep the backup for user to investigate
                pass
            raise e

    def cancel(self):
        """Cancel the conversion process"""
        self.cancelled = True


class DownloadManager(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Download URLs (official download links)
        self.avast_url = "https://www.avast.com/download-thank-you.php?product=AV-FREE-ONLINE&loc=en-us"
        self.virustotal_url = "https://www.virustotal.com/gui/home/upload"
        self.ccleaner_url = "https://www.ccleaner.com/ccleaner/download/standard"
        
    def init_ui(self):
        self.setWindowTitle("PC Utilities Manager")
        self.setGeometry(300, 300, 450, 400)
        self.setFixedSize(450, 400)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("PC Utilities Manager")
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

        # VirusTotal Button
        self.virustotal_button = QPushButton("Scan file with VirusTotal")
        self.virustotal_button.setStyleSheet("""
            QPushButton {
                background-color: #394EFF;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2D3FCC;
            }
            QPushButton:pressed {
                background-color: #2433A3;
            }
        """)
        self.virustotal_button.clicked.connect(self.open_virustotal)
        layout.addWidget(self.virustotal_button)

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

        # Office File Converter Button
        self.converter_button = QPushButton("Convert Office Files to Latest Format")
        self.converter_button.setStyleSheet("""
            QPushButton {
                background-color: #217346;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1A5C37;
            }
            QPushButton:pressed {
                background-color: #134528;
            }
        """)
        self.converter_button.clicked.connect(self.open_converter_dialog)
        layout.addWidget(self.converter_button)

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

    def open_virustotal(self):
        """Open VirusTotal file upload page"""
        self.status_label.setText("Opening VirusTotal...")
        try:
            webbrowser.open(self.virustotal_url)
            self.status_label.setText("VirusTotal opened in browser")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("VirusTotal Opened")
            msg.setText("VirusTotal file scanner opened!")
            msg.setInformativeText("You can now upload any file to scan it for viruses and malware.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        except Exception as e:
            self.status_label.setText(f"Error opening VirusTotal: {str(e)}")

    def show_download_message(self, app_name):
        """Show information message about the download"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Download Started")
        msg.setText(f"{app_name} download page opened!")
        msg.setInformativeText(f"The {app_name} download should start automatically in your browser.\nThe file will be saved to your Downloads folder.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def open_converter_dialog(self):
        """Open dialog to select conversion type"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Office File Converter")
        msg.setText("What would you like to convert?")
        msg.setInformativeText("Select a single file, a folder, or an entire drive to convert all Office files to the latest format.\n\nBackups will be created automatically.")

        file_btn = msg.addButton("Select File", QMessageBox.ActionRole)
        folder_btn = msg.addButton("Select Folder", QMessageBox.ActionRole)
        drive_btn = msg.addButton("Select Drive", QMessageBox.ActionRole)
        cancel_btn = msg.addButton(QMessageBox.Cancel)

        msg.exec()

        if msg.clickedButton() == file_btn:
            self.select_file_to_convert()
        elif msg.clickedButton() == folder_btn:
            self.select_folder_to_convert()
        elif msg.clickedButton() == drive_btn:
            self.select_drive_to_convert()

    def select_file_to_convert(self):
        """Select a single file to convert"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Office File to Convert",
            "",
            "Office Files (*.doc *.docx *.xls *.xlsx *.ppt *.pptx);;All Files (*.*)"
        )

        if file_path:
            self.start_conversion(file_path, is_file=True)

    def select_folder_to_convert(self):
        """Select a folder to convert all Office files in it"""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder to Convert Office Files",
            ""
        )

        if folder_path:
            self.start_conversion(folder_path, is_file=False)

    def select_drive_to_convert(self):
        """Select a drive to convert all Office files in it"""
        # Get available drives
        import string
        from pathlib import Path

        available_drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if Path(drive).exists():
                available_drives.append(drive)

        if not available_drives:
            QMessageBox.warning(self, "No Drives Found", "No accessible drives were found on this system.")
            return

        # Create selection dialog
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Select Drive")
        msg.setText("Select a drive to convert all Office files:")
        msg.setInformativeText("Warning: This may take a long time for large drives!")

        drive_buttons = []
        for drive in available_drives:
            btn = msg.addButton(drive, QMessageBox.ActionRole)
            drive_buttons.append((btn, drive))

        cancel_btn = msg.addButton(QMessageBox.Cancel)
        msg.exec()

        for btn, drive in drive_buttons:
            if msg.clickedButton() == btn:
                self.start_conversion(drive, is_file=False)
                break

    def start_conversion(self, path, is_file=False):
        """Start the conversion process with progress dialog"""
        self.status_label.setText("Preparing conversion...")

        # Create worker thread
        self.worker = ConversionWorker(path, is_file)

        # Create progress dialog
        self.progress_dialog = QProgressDialog("Initializing...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowTitle("Converting Office Files")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setValue(0)

        # Connect signals
        self.worker.progress.connect(self.update_conversion_progress)
        self.worker.finished.connect(self.conversion_finished)
        self.progress_dialog.canceled.connect(self.cancel_conversion)

        # Start conversion
        self.worker.start()

    def update_conversion_progress(self, current, total, current_file):
        """Update the progress dialog"""
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_dialog.setValue(percentage)
            self.progress_dialog.setMaximum(100)
            self.progress_dialog.setLabelText(f"Converting {current} of {total} files...\n\n{Path(current_file).name}")

    def cancel_conversion(self):
        """Cancel the conversion process"""
        if hasattr(self, 'worker'):
            self.worker.cancel()
            self.status_label.setText("Conversion cancelled")

    def conversion_finished(self, results):
        """Show conversion results"""
        self.progress_dialog.close()

        # Build result message
        message = f"Conversion Complete!\n\n"
        message += f"Files converted: {results['converted']}\n"
        message += f"Files skipped: {results['skipped']}\n"
        message += f"Errors: {results['errors']}\n"

        if results['error_details']:
            message += f"\nError details:\n"
            for error in results['error_details'][:5]:  # Show first 5 errors
                message += f"  - {error}\n"
            if len(results['error_details']) > 5:
                message += f"  ... and {len(results['error_details']) - 5} more errors\n"

        # Show result dialog
        msg = QMessageBox()
        if results['errors'] > 0:
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Conversion Completed with Errors")
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Conversion Completed Successfully")

        msg.setText(message)
        msg.setInformativeText("Backup files were created with .backup extension.\n\nYou can delete them once you've verified the converted files.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

        self.status_label.setText("Conversion complete!")


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
    
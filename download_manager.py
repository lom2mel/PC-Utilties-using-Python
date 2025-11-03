import sys
import os
import webbrowser
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                                QLabel, QMessageBox, QFileDialog, QProgressDialog,
                                QMenuBar)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QAction
import win32com.client
import pythoncom
import shutil
from datetime import datetime
from PIL import Image


class ImageToPdfWorker(QThread):
    """Worker thread for converting images to PDF"""
    progress = Signal(int, int, str)  # current, total, current_file
    finished = Signal(dict)  # results dictionary

    def __init__(self, image_files, output_path):
        super().__init__()
        self.image_files = image_files
        self.output_path = output_path
        self.cancelled = False

    def run(self):
        """Execute the image to PDF conversion"""
        results = {
            'success': False,
            'error': None,
            'output_path': self.output_path
        }

        try:
            # Convert images to PDF
            images = []

            for idx, image_file in enumerate(self.image_files):
                if self.cancelled:
                    results['error'] = "Conversion cancelled by user"
                    break

                self.progress.emit(idx + 1, len(self.image_files), str(image_file))

                try:
                    # Open and convert image
                    img = Image.open(image_file)

                    # Convert to RGB if necessary (PDF doesn't support RGBA or other modes)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # Create white background
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')

                    images.append(img)
                except Exception as e:
                    results['error'] = f"Error processing {Path(image_file).name}: {str(e)}"
                    break

            if images and not self.cancelled:
                # Save as PDF
                if len(images) == 1:
                    images[0].save(self.output_path, 'PDF', resolution=100.0)
                else:
                    images[0].save(
                        self.output_path,
                        'PDF',
                        resolution=100.0,
                        save_all=True,
                        append_images=images[1:]
                    )

                results['success'] = True

        except Exception as e:
            results['error'] = str(e)

        self.finished.emit(results)

    def cancel(self):
        """Cancel the conversion process"""
        self.cancelled = True


class ConversionWorker(QThread):
    """Worker thread for converting Office files"""
    progress = Signal(int, int, str)  # current, total, current_file
    sub_progress = Signal(str, int)  # status_message, percentage (0-100)
    finished = Signal(dict)  # results dictionary

    def __init__(self, path, is_file=False):
        super().__init__()
        self.path = path
        self.is_file = is_file
        self.cancelled = False
        self.archive_folder = self.create_archive_folder()
        self.files_to_archive = []  # Track old files and backups to move

    def create_archive_folder(self):
        """Create an archive folder on desktop for old and backup files"""
        desktop = Path.home() / "Desktop"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"Office_Archive_{timestamp}"
        archive_path = desktop / archive_name

        # Create the archive folder
        archive_path.mkdir(parents=True, exist_ok=True)

        return archive_path

    def run(self):
        """Execute the conversion process"""
        results = {
            'converted': 0,
            'skipped': 0,
            'errors': 0,
            'error_details': [],
            'archive_folder': str(self.archive_folder)
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

        # Move all archived files to the archive folder
        self.move_files_to_archive()

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
        """Convert a single Office file to the latest format using COM automation"""
        extension = file_path.suffix.lower()

        # Initialize COM for this thread
        pythoncom.CoInitialize()

        backup_path = None
        conversion_successful = False

        try:
            # Word documents
            if extension in ['.doc', '.docx']:
                word = None
                try:
                    self.sub_progress.emit("Initializing Microsoft Word...", 10)
                    word = win32com.client.Dispatch("Word.Application")
                    word.Visible = False
                    word.DisplayAlerts = False

                    # Open the document
                    self.sub_progress.emit(f"Opening {file_path.name}...", 25)
                    doc = word.Documents.Open(str(file_path.absolute()))

                    # Save as .docx (Office 365 format)
                    # wdFormatXMLDocument = 12 (docx format)
                    self.sub_progress.emit("Converting to latest format...", 50)
                    new_path = file_path.with_suffix('.docx')

                    self.sub_progress.emit("Saving converted file...", 75)
                    doc.SaveAs2(str(new_path.absolute()), FileFormat=12)
                    doc.Close()

                    conversion_successful = True

                    # If original was .doc, rename it to .backup and archive it
                    if extension == '.doc' and file_path != new_path:
                        self.sub_progress.emit("Creating backup...", 90)
                        backup_path = file_path.with_suffix('.doc.backup')
                        file_path.rename(backup_path)
                        self.files_to_archive.append(backup_path)

                    self.sub_progress.emit("Completed!", 100)
                    return True
                finally:
                    if word:
                        word.Quit()

            # Excel spreadsheets
            elif extension in ['.xls', '.xlsx']:
                excel = None
                try:
                    self.sub_progress.emit("Initializing Microsoft Excel...", 10)
                    excel = win32com.client.Dispatch("Excel.Application")
                    excel.Visible = False
                    excel.DisplayAlerts = False

                    # Open the workbook
                    self.sub_progress.emit(f"Opening {file_path.name}...", 25)
                    wb = excel.Workbooks.Open(str(file_path.absolute()))

                    # Save as .xlsx (Office 365 format)
                    # xlOpenXMLWorkbook = 51 (xlsx format)
                    self.sub_progress.emit("Converting to latest format...", 50)
                    new_path = file_path.with_suffix('.xlsx')

                    self.sub_progress.emit("Saving converted file...", 75)
                    wb.SaveAs(str(new_path.absolute()), FileFormat=51)
                    wb.Close()

                    conversion_successful = True

                    # If original was .xls, rename it to .backup and archive it
                    if extension == '.xls' and file_path != new_path:
                        self.sub_progress.emit("Creating backup...", 90)
                        backup_path = file_path.with_suffix('.xls.backup')
                        file_path.rename(backup_path)
                        self.files_to_archive.append(backup_path)

                    self.sub_progress.emit("Completed!", 100)
                    return True
                finally:
                    if excel:
                        excel.Quit()

            # PowerPoint presentations
            elif extension in ['.ppt', '.pptx']:
                powerpoint = None
                try:
                    self.sub_progress.emit("Initializing Microsoft PowerPoint...", 10)
                    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
                    powerpoint.Visible = False
                    powerpoint.DisplayAlerts = False

                    # Open the presentation
                    self.sub_progress.emit(f"Opening {file_path.name}...", 25)
                    prs = powerpoint.Presentations.Open(str(file_path.absolute()), WithWindow=False)

                    # Save as .pptx (Office 365 format)
                    # ppSaveAsOpenXMLPresentation = 24 (pptx format)
                    self.sub_progress.emit("Converting to latest format...", 50)
                    new_path = file_path.with_suffix('.pptx')

                    self.sub_progress.emit("Saving converted file...", 75)
                    prs.SaveAs(str(new_path.absolute()), FileFormat=24)
                    prs.Close()

                    conversion_successful = True

                    # If original was .ppt, rename it to .backup and archive it
                    if extension == '.ppt' and file_path != new_path:
                        self.sub_progress.emit("Creating backup...", 90)
                        backup_path = file_path.with_suffix('.ppt.backup')
                        file_path.rename(backup_path)
                        self.files_to_archive.append(backup_path)

                    self.sub_progress.emit("Completed!", 100)
                    return True
                finally:
                    if powerpoint:
                        powerpoint.Quit()

            return False

        except Exception as e:
            # If conversion failed and we created a backup, restore the original
            if backup_path and backup_path.exists() and not conversion_successful:
                backup_path.rename(file_path)
            raise e
        finally:
            # Uninitialize COM
            pythoncom.CoUninitialize()

    def move_files_to_archive(self):
        """Move all backup and old files to the archive folder"""
        for file_path in self.files_to_archive:
            if file_path.exists():
                try:
                    # Preserve the relative directory structure in the archive
                    # Get the parent directory name to avoid name conflicts
                    parent_name = file_path.parent.name
                    dest_dir = self.archive_folder / parent_name
                    dest_dir.mkdir(parents=True, exist_ok=True)

                    dest_path = dest_dir / file_path.name

                    # Handle name conflicts by adding a number
                    counter = 1
                    original_dest = dest_path
                    while dest_path.exists():
                        dest_path = original_dest.parent / f"{original_dest.stem}_{counter}{original_dest.suffix}"
                        counter += 1

                    # Move the file
                    shutil.move(str(file_path), str(dest_path))
                except Exception:
                    # If we can't move a file, just skip it
                    pass

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

        # Create menu bar
        menu_bar = QMenuBar(self)
        help_menu = menu_bar.addMenu("Help")

        # Add About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        layout = QVBoxLayout()
        layout.setMenuBar(menu_bar)
        
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

        # Picture to PDF Converter Button
        self.picture_to_pdf_button = QPushButton("Convert Pictures to PDF")
        self.picture_to_pdf_button.setStyleSheet("""
            QPushButton {
                background-color: #D83B01;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #C13200;
            }
            QPushButton:pressed {
                background-color: #A32900;
            }
        """)
        self.picture_to_pdf_button.clicked.connect(self.open_picture_to_pdf_dialog)
        layout.addWidget(self.picture_to_pdf_button)

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

    def show_about(self):
        """Show About dialog"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("About PC Utilities Manager")
        msg.setText("PC Utilities Manager")
        msg.setInformativeText(
            "Version 1.0\n\n"
            "A simple utility application for managing PC maintenance tools "
            "and converting Office files to the latest format.\n\n"
            "Created by: Lomel A. Arguelles\n\n"
            "© 2025"
        )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def check_office_installed(self):
        """Check if Microsoft Office is installed"""
        try:
            pythoncom.CoInitialize()
            # Try to create Word instance
            word = win32com.client.Dispatch("Word.Application")
            word.Quit()
            pythoncom.CoUninitialize()
            return True
        except:
            pythoncom.CoUninitialize()
            return False

    def open_converter_dialog(self):
        """Open dialog to select conversion type"""
        # Check if Microsoft Office is installed
        if not self.check_office_installed():
            QMessageBox.critical(
                self,
                "Microsoft Office Required",
                "Microsoft Office must be installed on this computer to use the file converter.\n\n"
                "This feature uses Microsoft Office COM automation to convert files to the latest format.\n\n"
                "Please install Microsoft Office and try again."
            )
            return

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
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)

        # Connect signals
        self.worker.progress.connect(self.update_conversion_progress)
        self.worker.sub_progress.connect(self.update_sub_progress)
        self.worker.finished.connect(self.conversion_finished)
        self.progress_dialog.canceled.connect(self.cancel_conversion)

        # Start conversion
        self.worker.start()

    def update_conversion_progress(self, current, total, current_file):
        """Update the progress dialog with overall progress"""
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_dialog.setValue(percentage)
            self.progress_dialog.setMaximum(100)
            # Store current file info for sub-progress updates
            self.current_file_name = Path(current_file).name
            self.current_file_num = current
            self.total_files = total
            # Initial message before sub-progress starts
            self.progress_dialog.setLabelText(
                f"File {current} of {total}: {self.current_file_name}\n\n"
                f"Preparing..."
            )

    def update_sub_progress(self, status_message, sub_percentage):
        """Update the progress dialog with sub-task progress"""
        if hasattr(self, 'current_file_num') and hasattr(self, 'total_files'):
            # Combine overall progress with sub-progress for smoother visual feedback
            overall_percentage = int(((self.current_file_num - 1) / self.total_files) * 100)
            file_weight = 100 / self.total_files
            combined_percentage = int(overall_percentage + (sub_percentage / 100) * file_weight)

            self.progress_dialog.setValue(combined_percentage)
            self.progress_dialog.setLabelText(
                f"File {self.current_file_num} of {self.total_files}: {self.current_file_name}\n\n"
                f"{status_message}\n"
                f"Progress: {sub_percentage}%"
            )

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

        # Update informative text to include archive folder location
        archive_folder = results.get('archive_folder', 'Desktop')
        info_text = f"Backup files (.backup) have been moved to:\n{archive_folder}\n\n"
        info_text += "All backup files are organized in this folder on your Desktop.\n"
        info_text += "Your working directories now contain only the new format files (.docx, .xlsx, .pptx).\n\n"
        info_text += "You can delete the archive folder once you've verified the converted files work correctly."

        msg.setInformativeText(info_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

        self.status_label.setText("Conversion complete!")

    def open_picture_to_pdf_dialog(self):
        """Open dialog to select images and convert to PDF"""
        # Select image files
        file_dialog = QFileDialog()
        image_files, _ = file_dialog.getOpenFileNames(
            self,
            "Select Images to Convert to PDF",
            "",
            "Image Files (*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif);;All Files (*.*)"
        )

        if not image_files:
            return

        # Ask for output PDF location
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF As",
            str(Path.home() / "Desktop" / "converted_images.pdf"),
            "PDF Files (*.pdf)"
        )

        if not output_path:
            return

        # Ensure .pdf extension
        if not output_path.lower().endswith('.pdf'):
            output_path += '.pdf'

        # Start conversion
        self.start_picture_to_pdf_conversion(image_files, output_path)

    def start_picture_to_pdf_conversion(self, image_files, output_path):
        """Start the image to PDF conversion process"""
        self.status_label.setText("Converting images to PDF...")

        # Create worker thread
        self.image_worker = ImageToPdfWorker(image_files, output_path)

        # Create progress dialog
        self.image_progress_dialog = QProgressDialog(
            "Initializing...",
            "Cancel",
            0,
            len(image_files),
            self
        )
        self.image_progress_dialog.setWindowTitle("Converting Images to PDF")
        self.image_progress_dialog.setWindowModality(Qt.WindowModal)
        self.image_progress_dialog.setMinimumDuration(0)
        self.image_progress_dialog.setValue(0)
        self.image_progress_dialog.setAutoClose(False)
        self.image_progress_dialog.setAutoReset(False)

        # Connect signals
        self.image_worker.progress.connect(self.update_image_conversion_progress)
        self.image_worker.finished.connect(self.image_conversion_finished)
        self.image_progress_dialog.canceled.connect(self.cancel_image_conversion)

        # Start conversion
        self.image_worker.start()

    def update_image_conversion_progress(self, current, total, current_file):
        """Update the progress dialog for image conversion"""
        self.image_progress_dialog.setValue(current)
        self.image_progress_dialog.setLabelText(
            f"Processing image {current} of {total}:\n{Path(current_file).name}"
        )

    def cancel_image_conversion(self):
        """Cancel the image conversion process"""
        if hasattr(self, 'image_worker'):
            self.image_worker.cancel()
            self.status_label.setText("Image conversion cancelled")

    def image_conversion_finished(self, results):
        """Show image conversion results"""
        self.image_progress_dialog.close()

        if results['success']:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Conversion Successful")
            msg.setText("Images successfully converted to PDF!")
            msg.setInformativeText(f"PDF saved to:\n{results['output_path']}")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            self.status_label.setText("Image conversion complete!")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Conversion Failed")
            msg.setText("Failed to convert images to PDF")
            msg.setInformativeText(f"Error: {results['error']}")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            self.status_label.setText("Image conversion failed")


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
    
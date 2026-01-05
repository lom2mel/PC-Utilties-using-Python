"""Modern redesigned UI for PC Utilities Manager with professional UX."""

import webbrowser
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QMessageBox,
    QFileDialog,
    QProgressDialog,
    QFrame,
    QScrollArea,
    QMenuBar,
    QMainWindow,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QPalette, QColor, QAction, QKeySequence
import pythoncom
import win32com.client

from features.image_converter.worker import ImageToPdfWorker
from features.office_converter.worker import ConversionWorker


class ModernCard(QFrame):
    """Modern card widget with hover effects."""

    def __init__(self, title: str, description: str, icon_text: str, color: str):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            ModernCard {{
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                padding: 20px;
            }}
            ModernCard:hover {{
                border: 2px solid {color};
                background-color: #FAFAFA;
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)
        self.setup_ui(title, description, icon_text, color)

    def setup_ui(self, title: str, description: str, icon_text: str, color: str):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Icon area
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                border-radius: 30px;
                font-size: 28px;
                font-weight: bold;
                padding: 15px;
            }}
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedSize(60, 60)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title_label.setStyleSheet("color: #1F1F1F;")
        title_label.setWordWrap(True)

        # Description
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 9))
        desc_label.setStyleSheet("color: #666666;")
        desc_label.setWordWrap(True)

        layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()

        self.setLayout(layout)


class SectionHeader(QWidget):
    """Section header with title and description."""

    def __init__(self, title: str, description: str = ""):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setStyleSheet("color: #1F1F1F;")

        layout.addWidget(title_label)

        if description:
            desc_label = QLabel(description)
            desc_label.setFont(QFont("Segoe UI", 9))
            desc_label.setStyleSheet("color: #666666;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        self.setLayout(layout)


class ModernDownloadManager(QMainWindow):
    """Modern redesigned PC Utilities Manager with professional UI/UX."""

    def __init__(self):
        super().__init__()
        self.init_ui()

        # Download URLs
        self.avast_url = (
            "https://www.avast.com/download-thank-you.php?product=AV-FREE-ONLINE"
            "&loc=en-us"
        )
        self.virustotal_url = "https://www.virustotal.com/gui/home/upload"
        self.ccleaner_url = "https://www.ccleaner.com/ccleaner/download/standard"
        self.speccy_url = "https://www.ccleaner.com/speccy/download/standard"

    def init_ui(self):
        """Initialize modern UI with card-based layout."""
        self.setWindowTitle("PC Utilities Manager")
        self.setMinimumSize(900, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)

        # Create menu bar
        self.create_menu_bar()

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout with scroll area
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header section
        header = self.create_header()
        main_layout.addWidget(header)

        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(30)

        # Status indicator
        self.status_indicator = self.create_status_indicator()
        content_layout.addWidget(self.status_indicator)

        # Security Tools Section
        security_section = self.create_security_section()
        content_layout.addWidget(security_section)

        # File Converters Section
        converters_section = self.create_converters_section()
        content_layout.addWidget(converters_section)

        content_layout.addStretch()

        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        central_widget.setLayout(main_layout)

    def create_menu_bar(self):
        """Create menu bar with File and Help menus."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        # Office Converter action
        converter_action = QAction("&Office File Converter", self)
        converter_action.setShortcut(QKeySequence("Ctrl+O"))
        converter_action.setStatusTip("Convert Office files to latest format")
        converter_action.triggered.connect(self.open_converter_dialog)
        file_menu.addAction(converter_action)

        # Picture to PDF action
        pdf_action = QAction("&Picture to PDF", self)
        pdf_action.setShortcut(QKeySequence("Ctrl+P"))
        pdf_action.setStatusTip("Convert images to PDF")
        pdf_action.triggered.connect(self.open_picture_to_pdf_dialog)
        file_menu.addAction(pdf_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        # About action
        about_action = QAction("&About", self)
        about_action.setShortcut(QKeySequence("F1"))
        about_action.setStatusTip("About this application")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_header(self) -> QWidget:
        """Create modern header with branding."""
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667EEA, stop:1 #764BA2
                );
                border-bottom: 3px solid rgba(255, 255, 255, 0.2);
            }
        """)
        header.setFixedHeight(120)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)

        # Title
        title = QLabel("🛠️ PC Utilities Manager")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel(
            "Essential tools for system maintenance, security, and file management"
        )
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: "
                              "transparent;")
        layout.addWidget(subtitle)

        # About button
        about_btn = QPushButton("About")
        about_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        about_btn.clicked.connect(self.show_about)
        about_btn.setMinimumWidth(80)
        about_btn.setMinimumHeight(36)
        layout.addWidget(about_btn, alignment=Qt.AlignRight | Qt.AlignTop)

        header.setLayout(layout)
        return header

    def create_status_indicator(self) -> QWidget:
        """Create modern status indicator."""
        status_widget = QWidget()
        status_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)

        # Status icon
        icon = QLabel("✓")
        icon.setFont(QFont("Segoe UI", 16, QFont.Bold))
        icon.setStyleSheet("color: #4CAF50; background: transparent;")

        # Status text
        self.status_label = QLabel("Ready to use")
        self.status_label.setFont(QFont("Segoe UI", 11))
        self.status_label.setStyleSheet("color: #1F1F1F; background: transparent;")

        layout.addWidget(icon)
        layout.addWidget(self.status_label)
        layout.addStretch()

        status_widget.setLayout(layout)
        return status_widget

    def create_security_section(self) -> QWidget:
        """Create security tools section with cards."""
        section = QWidget()
        section.setStyleSheet("background: transparent;")
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Section header
        header = SectionHeader(
            "🔒 Security & Maintenance Tools",
            "Download and use essential security utilities to keep your PC safe"
        )
        layout.addWidget(header)

        # Cards grid
        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)

        # Avast card
        avast_card = ModernCard(
            "Avast Antivirus",
            "Download free antivirus protection for your PC",
            "🛡️",
            "#FF6600"
        )
        avast_card.mousePressEvent = lambda e: self.download_avast()
        cards_layout.addWidget(avast_card, 0, 0)

        # VirusTotal card
        virustotal_card = ModernCard(
            "VirusTotal Scanner",
            "Scan files for viruses and malware online",
            "🔍",
            "#394EFF"
        )
        virustotal_card.mousePressEvent = lambda e: self.open_virustotal()
        cards_layout.addWidget(virustotal_card, 0, 1)

        # CCleaner card
        ccleaner_card = ModernCard(
            "CCleaner",
            "Clean and optimize your PC performance",
            "🧹",
            "#0066CC"
        )
        ccleaner_card.mousePressEvent = lambda e: self.download_ccleaner()
        cards_layout.addWidget(ccleaner_card, 0, 2)

        # Speccy card
        speccy_card = ModernCard(
            "Speccy",
            "View detailed system information and specifications",
            "💻",
            "#00A4EF"
        )
        speccy_card.mousePressEvent = lambda e: self.download_speccy()
        cards_layout.addWidget(speccy_card, 1, 0)

        layout.addLayout(cards_layout)
        section.setLayout(layout)
        return section

    def create_converters_section(self) -> QWidget:
        """Create file converters section with cards."""
        section = QWidget()
        section.setStyleSheet("background: transparent;")
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Section header
        header = SectionHeader(
            "📁 File Converters",
            "Convert your documents and images to modern formats"
        )
        layout.addWidget(header)

        # Cards grid
        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)

        # Office converter card
        office_card = ModernCard(
            "Office File Converter",
            "Convert old Office files to latest format (.docx, .xlsx, .pptx)",
            "📄",
            "#217346"
        )
        office_card.mousePressEvent = lambda e: self.open_converter_dialog()
        cards_layout.addWidget(office_card, 0, 0)

        # Picture to PDF card
        pdf_card = ModernCard(
            "Picture to PDF",
            "Convert images to PDF documents quickly and easily",
            "🖼️",
            "#D83B01"
        )
        pdf_card.mousePressEvent = lambda e: self.open_picture_to_pdf_dialog()
        cards_layout.addWidget(pdf_card, 0, 1)

        # Placeholder for future feature
        placeholder_card = QFrame()
        placeholder_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px dashed #E0E0E0;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        placeholder_layout = QVBoxLayout()
        placeholder_text = QLabel("More tools\ncoming soon...")
        placeholder_text.setFont(QFont("Segoe UI", 11))
        placeholder_text.setStyleSheet("color: #999999;")
        placeholder_text.setAlignment(Qt.AlignCenter)
        placeholder_layout.addWidget(placeholder_text)
        placeholder_card.setLayout(placeholder_layout)
        cards_layout.addWidget(placeholder_card, 0, 2)

        layout.addLayout(cards_layout)
        section.setLayout(layout)
        return section

    def update_status(self, message: str, success: bool = True):
        """Update status indicator with message."""
        icon = "✓" if success else "⚠"
        color = "#4CAF50" if success else "#FF9800"
        
        # Find and update icon in status_indicator
        icon_label = self.status_indicator.findChild(QLabel)
        if icon_label:
            icon_label.setText(icon)
            icon_label.setStyleSheet(f"color: {color}; background: transparent;")
        
        self.status_label.setText(message)

    def download_avast(self):
        """Download Avast Antivirus."""
        self.update_status("Opening Avast download page...")
        try:
            webbrowser.open(self.avast_url)
            self.update_status("Avast download page opened in browser")
            self.show_download_message("Avast Antivirus")
        except Exception as e:
            self.update_status(f"Error: {str(e)}", success=False)

    def download_ccleaner(self):
        """Download CCleaner."""
        self.update_status("Opening CCleaner download page...")
        try:
            webbrowser.open(self.ccleaner_url)
            self.update_status("CCleaner download page opened in browser")
            self.show_download_message("CCleaner")
        except Exception as e:
            self.update_status(f"Error: {str(e)}", success=False)

    def download_speccy(self):
        """Download Speccy."""
        self.update_status("Opening Speccy download page...")
        try:
            webbrowser.open(self.speccy_url)
            self.update_status("Speccy download page opened in browser")
            self.show_download_message("Speccy")
        except Exception as e:
            self.update_status(f"Error: {str(e)}", success=False)

    def open_virustotal(self):
        """Open VirusTotal."""
        self.update_status("Opening VirusTotal...")
        try:
            webbrowser.open(self.virustotal_url)
            self.update_status("VirusTotal opened in browser")
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
            self.update_status(f"Error: {str(e)}", success=False)

    def show_download_message(self, app_name: str):
        """Show download message."""
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

    def show_about(self):
        """Show About dialog."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("About PC Utilities Manager")
        msg.setText("PC Utilities Manager")
        msg.setInformativeText(
            "Version 2.0 - Modern UI\n\n"
            "A modern utility application for managing PC maintenance tools "
            "and converting files to the latest formats.\n\n"
            "Created by: Lomel A. Arguelles\n"
            "© 2025\n\n"
            "---\n\n"
            "This application uses PySide6 (Qt for Python),\n"
            "licensed under the GNU Lesser General Public License v3.0.\n\n"
            "PySide6 Repository:\n"
            "https://code.qt.io/cgit/pyside/pyside-setup.git/\n\n"
            "For license details, see LICENSE.txt included with this application."
        )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def check_office_installed(self) -> bool:
        """Check if Microsoft Office is installed."""
        try:
            pythoncom.CoInitialize()
            word = win32com.client.Dispatch("Word.Application")
            word.Quit()
            pythoncom.CoUninitialize()
            return True
        except Exception:
            pythoncom.CoUninitialize()
            return False

    def open_converter_dialog(self):
        """Open Office converter dialog."""
        if not self.check_office_installed():
            QMessageBox.critical(
                self,
                "Microsoft Office Required",
                "Microsoft Office must be installed on this computer to use the file "
                "converter.\n\nThis feature uses Microsoft Office COM automation to "
                "convert files to the latest format.\n\nPlease install Microsoft "
                "Office and try again.",
            )
            return

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Office File Converter")
        msg.setText("What would you like to convert?")
        msg.setInformativeText(
            "Select a single file, a folder, or an entire drive to convert all Office "
            "files to the latest format.\n\nBackups will be created automatically."
        )

        file_btn = msg.addButton("Select File", QMessageBox.ActionRole)
        folder_btn = msg.addButton("Select Folder", QMessageBox.ActionRole)
        drive_btn = msg.addButton("Select Drive", QMessageBox.ActionRole)
        msg.addButton(QMessageBox.Cancel)

        msg.exec()

        if msg.clickedButton() == file_btn:
            self.select_file_to_convert()
        elif msg.clickedButton() == folder_btn:
            self.select_folder_to_convert()
        elif msg.clickedButton() == drive_btn:
            self.select_drive_to_convert()

    def select_file_to_convert(self):
        """Select single file to convert."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Office File to Convert",
            "",
            "Office Files (*.doc *.docx *.xls *.xlsx *.ppt *.pptx);;All Files (*.*)",
        )

        if file_path:
            self.start_conversion(file_path, is_file=True)

    def select_folder_to_convert(self):
        """Select folder to convert."""
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Folder to Convert Office Files", ""
        )

        if folder_path:
            self.start_conversion(folder_path, is_file=False)

    def select_drive_to_convert(self):
        """Select drive to convert."""
        import string

        available_drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\\\"
            if Path(drive).exists():
                available_drives.append(drive)

        if not available_drives:
            QMessageBox.warning(
                self,
                "No Drives Found",
                "No accessible drives were found on this system.",
            )
            return

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Select Drive")
        msg.setText("Select a drive to convert all Office files:")
        msg.setInformativeText("Warning: This may take a long time for large drives!")

        drive_buttons = []
        for drive in available_drives:
            btn = msg.addButton(drive, QMessageBox.ActionRole)
            drive_buttons.append((btn, drive))

        msg.addButton(QMessageBox.Cancel)
        msg.exec()

        for btn, drive in drive_buttons:
            if msg.clickedButton() == btn:
                self.start_conversion(drive, is_file=False)
                break

    def start_conversion(self, path: str, is_file: bool = False):
        """Start conversion process."""
        self.update_status("Preparing conversion...")

        self.worker = ConversionWorker(path, is_file)

        self.progress_dialog = QProgressDialog(
            "Initializing...", "Cancel", 0, 100, self
        )
        self.progress_dialog.setWindowTitle("Converting Office Files")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setValue(0)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)

        self.worker.progress.connect(self.update_conversion_progress)
        self.worker.sub_progress.connect(self.update_sub_progress)
        self.worker.finished.connect(self.conversion_finished)
        self.progress_dialog.canceled.connect(self.cancel_conversion)

        self.worker.start()

    def update_conversion_progress(self, current: int, total: int, current_file: str):
        """Update conversion progress."""
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_dialog.setValue(percentage)
            self.progress_dialog.setMaximum(100)
            self.current_file_name = Path(current_file).name
            self.current_file_num = current
            self.total_files = total
            self.progress_dialog.setLabelText(
                f"File {current} of {total}: {self.current_file_name}\n\nPreparing..."
            )

    def update_sub_progress(self, status_message: str, sub_percentage: int):
        """Update sub-progress."""
        if hasattr(self, "current_file_num") and hasattr(self, "total_files"):
            overall_percentage = int(
                ((self.current_file_num - 1) / self.total_files) * 100
            )
            file_weight = 100 / self.total_files
            combined_percentage = int(
                overall_percentage + (sub_percentage / 100) * file_weight
            )

            self.progress_dialog.setValue(combined_percentage)
            self.progress_dialog.setLabelText(
                f"File {self.current_file_num} of {self.total_files}: "
                f"{self.current_file_name}\n\n"
                f"{status_message}\n"
                f"Progress: {sub_percentage}%"
            )

    def cancel_conversion(self):
        """Cancel conversion."""
        if hasattr(self, "worker"):
            self.worker.cancel()
            self.update_status("Conversion cancelled", success=False)

    def conversion_finished(self, results: dict):
        """Show conversion results."""
        self.progress_dialog.close()

        message = "Conversion Complete!\n\n"
        message += f"Files converted: {results['converted']}\n"
        message += f"Files skipped: {results['skipped']}\n"
        message += f"Errors: {results['errors']}\n"

        if results["error_details"]:
            message += "\nError details:\n"
            for error in results["error_details"][:5]:
                message += f"  - {error}\n"
            if len(results["error_details"]) > 5:
                message += f"  ... and {len(results['error_details']) - 5} more errors\n"

        msg = QMessageBox()
        if results["errors"] > 0:
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Conversion Completed with Errors")
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Conversion Completed Successfully")

        msg.setText(message)

        archive_folder = results.get("archive_folder", "Desktop")
        info_text = f"Backup files (.backup) have been moved to:\n{archive_folder}\n\n"
        info_text += "Your working directories now contain only the new format files "
        info_text += "(.docx, .xlsx, .pptx).\n\n"
        info_text += "You can delete the archive folder once you've verified the "
        info_text += "converted files work correctly."

        msg.setInformativeText(info_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

        self.update_status("Conversion complete!")

    def open_picture_to_pdf_dialog(self):
        """Open picture to PDF converter."""
        file_dialog = QFileDialog()
        image_files, _ = file_dialog.getOpenFileNames(
            self,
            "Select Images to Convert to PDF",
            "",
            "Image Files (*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif);;All Files (*.*)",
        )

        if not image_files:
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF As",
            str(Path.home() / "Desktop" / "converted_images.pdf"),
            "PDF Files (*.pdf)",
        )

        if not output_path:
            return

        if not output_path.lower().endswith(".pdf"):
            output_path += ".pdf"

        self.start_picture_to_pdf_conversion(image_files, output_path)

    def start_picture_to_pdf_conversion(self, image_files: list, output_path: str):
        """Start picture to PDF conversion."""
        self.update_status("Converting images to PDF...")

        self.image_worker = ImageToPdfWorker(image_files, output_path)

        self.image_progress_dialog = QProgressDialog(
            "Initializing...", "Cancel", 0, len(image_files), self
        )
        self.image_progress_dialog.setWindowTitle("Converting Images to PDF")
        self.image_progress_dialog.setWindowModality(Qt.WindowModal)
        self.image_progress_dialog.setMinimumDuration(0)
        self.image_progress_dialog.setValue(0)
        self.image_progress_dialog.setAutoClose(False)
        self.image_progress_dialog.setAutoReset(False)

        self.image_worker.progress.connect(self.update_image_conversion_progress)
        self.image_worker.finished.connect(self.image_conversion_finished)
        self.image_progress_dialog.canceled.connect(self.cancel_image_conversion)

        self.image_worker.start()

    def update_image_conversion_progress(
        self, current: int, total: int, current_file: str
    ):
        """Update image conversion progress."""
        self.image_progress_dialog.setValue(current)
        self.image_progress_dialog.setLabelText(
            f"Processing image {current} of {total}:\n{Path(current_file).name}"
        )

    def cancel_image_conversion(self):
        """Cancel image conversion."""
        if hasattr(self, "image_worker"):
            self.image_worker.cancel()
            self.update_status("Image conversion cancelled", success=False)

    def image_conversion_finished(self, results: dict):
        """Show image conversion results."""
        self.image_progress_dialog.close()

        if results["success"]:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Conversion Successful")
            msg.setText("Images successfully converted to PDF!")
            msg.setInformativeText(f"PDF saved to:\n{results['output_path']}")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            self.update_status("Image conversion complete!")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Conversion Failed")
            msg.setText("Failed to convert images to PDF")
            msg.setInformativeText(f"Error: {results['error']}")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            self.update_status("Image conversion failed", success=False)

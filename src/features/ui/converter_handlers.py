"""File converter handlers for Office documents and images.

This module contains handlers for converting Office files to modern formats
and converting images to PDF documents.
"""

import string
from pathlib import Path
from PySide6.QtWidgets import (
    QMessageBox,
    QFileDialog,
    QProgressDialog,
)
from PySide6.QtCore import Qt, QObject, Signal
import pythoncom
import win32com.client

from features.image_converter.worker import ImageToPdfWorker
from features.office_converter.worker import ConversionWorker


class ConverterHandlers(QObject):
    """Handlers for file conversion operations.

    Manages Office file conversion to modern formats and image to PDF conversion.

    Signals:
        status_changed: Emitted when conversion status changes (message, success)
    """

    status_changed = Signal(str, bool)

    def check_office_installed(self) -> bool:
        """Check if Microsoft Office is installed.

        Returns:
            True if Office is available, False otherwise
        """
        try:
            pythoncom.CoInitialize()
            word = win32com.client.Dispatch("Word.Application")
            word.Quit()
            pythoncom.CoUninitialize()
            return True
        except Exception:
            pythoncom.CoUninitialize()
            return False

    def show_office_not_installed_error(self, parent) -> None:
        """Show error message when Office is not installed.

        Args:
            parent: Parent widget for the message dialog
        """
        QMessageBox.critical(
            parent,
            "Microsoft Office Required",
            "Microsoft Office must be installed on this computer to use the file "
            "converter.\n\nThis feature uses Microsoft Office COM automation to "
            "convert files to the latest format.\n\nPlease install Microsoft "
            "Office and try again.",
        )

    def open_converter_dialog(self, parent, callbacks: dict) -> None:
        """Open Office converter dialog with conversion options.

        Args:
            parent: Parent widget for dialogs
            callbacks: Dictionary mapping 'file', 'folder', 'drive' to handler functions
        """
        if not self.check_office_installed():
            self.show_office_not_installed_error(parent)
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
            callbacks['file']()
        elif msg.clickedButton() == folder_btn:
            callbacks['folder']()
        elif msg.clickedButton() == drive_btn:
            callbacks['drive']()

    def select_file_to_convert(self, parent, start_callback) -> None:
        """Open file dialog to select a single Office file.

        Args:
            parent: Parent widget for the dialog
            start_callback: Function to call with selected file path
        """
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Select Office File to Convert",
            "",
            "Office Files (*.doc *.docx *.xls *.xlsx *.ppt *.pptx);;All Files (*.*)",
        )

        if file_path:
            start_callback(file_path, is_file=True)

    def select_folder_to_convert(self, parent, start_callback) -> None:
        """Open folder dialog to select a folder for batch conversion.

        Args:
            parent: Parent widget for the dialog
            start_callback: Function to call with selected folder path
        """
        folder_path = QFileDialog.getExistingDirectory(
            parent, "Select Folder to Convert Office Files", ""
        )

        if folder_path:
            start_callback(folder_path, is_file=False)

    def select_drive_to_convert(self, parent, start_callback) -> None:
        """Open dialog to select a drive for conversion.

        Args:
            parent: Parent widget for the dialog
            start_callback: Function to call with selected drive path
        """
        available_drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if Path(drive).exists():
                available_drives.append(drive)

        if not available_drives:
            QMessageBox.warning(
                parent,
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
                start_callback(drive, is_file=False)
                break

    def start_conversion(
        self,
        parent,
        path: str,
        is_file: bool = False,
    ) -> None:
        """Start the Office file conversion process.

        Args:
            parent: Parent widget for progress dialog
            path: File or folder path to convert
            is_file: True if path is a single file, False for folder/drive
        """
        self.status_changed.emit("Preparing conversion...", True)

        worker = ConversionWorker(path, is_file)

        progress_dialog = QProgressDialog(
            "Initializing...", "Cancel", 0, 100, parent
        )
        progress_dialog.setWindowTitle("Converting Office Files")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setValue(0)
        progress_dialog.setAutoClose(False)
        progress_dialog.setAutoReset(False)

        worker.progress.connect(
            lambda curr, tot, file: self._update_conversion_progress(
                progress_dialog, curr, tot, file
            )
        )
        worker.sub_progress.connect(
            lambda msg, pct: self._update_sub_progress(
                progress_dialog, msg, pct
            )
        )
        worker.finished.connect(lambda res: self._conversion_finished(progress_dialog, res))
        progress_dialog.canceled.connect(worker.cancel)

        worker.start()

    def _update_conversion_progress(
        self,
        dialog: QProgressDialog,
        current: int,
        total: int,
        current_file: str,
    ) -> None:
        """Update conversion progress dialog.

        Args:
            dialog: Progress dialog to update
            current: Current file number
            total: Total number of files
            current_file: Current file path
        """
        if total > 0:
            percentage = int((current / total) * 100)
            dialog.setValue(percentage)
            dialog.setMaximum(100)
            current_file_name = Path(current_file).name
            dialog.setLabelText(
                f"File {current} of {total}: {current_file_name}\n\nPreparing..."
            )

    def _update_sub_progress(
        self,
        dialog: QProgressDialog,
        status_message: str,
        sub_percentage: int,
    ) -> None:
        """Update sub-progress during file conversion.

        Args:
            dialog: Progress dialog to update
            status_message: Status message to display
            sub_percentage: Sub-task progress percentage
        """
        label_text = dialog.labelText()
        if "File" in label_text:
            parts = label_text.split("\n\n")
            if len(parts) >= 1:
                file_info = parts[0]

                # Extract file numbers
                if " of " in file_info:
                    file_part = file_info.split(": ")[0]
                    try:
                        current_num = int(file_part.split(" ")[1])
                        total_num = int(file_part.split(" ")[3])

                        overall_percentage = int(((current_num - 1) / total_num) * 100)
                        file_weight = 100 / total_num
                        combined_percentage = int(
                            overall_percentage + (sub_percentage / 100) * file_weight
                        )

                        dialog.setValue(combined_percentage)
                        dialog.setLabelText(
                            f"{file_info}\n\n"
                            f"{status_message}\n"
                            f"Progress: {sub_percentage}%"
                        )
                    except (ValueError, IndexError):
                        dialog.setLabelText(f"{file_info}\n\n{status_message}")

    def _conversion_finished(self, dialog: QProgressDialog, results: dict) -> None:
        """Handle conversion completion.

        Args:
            dialog: Progress dialog to close
            results: Dictionary with conversion results
        """
        dialog.close()

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

        self.status_changed.emit("Conversion complete!", True)

    def open_picture_to_pdf_dialog(self, parent, start_callback) -> None:
        """Open dialog for selecting images to convert to PDF.

        Args:
            parent: Parent widget for dialogs
            start_callback: Function to call with selected images and output path
        """
        file_dialog = QFileDialog()
        image_files, _ = file_dialog.getOpenFileNames(
            parent,
            "Select Images to Convert to PDF",
            "",
            "Image Files (*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif);;All Files (*.*)",
        )

        if not image_files:
            return

        output_path, _ = QFileDialog.getSaveFileName(
            parent,
            "Save PDF As",
            str(Path.home() / "Desktop" / "converted_images.pdf"),
            "PDF Files (*.pdf)",
        )

        if not output_path:
            return

        if not output_path.lower().endswith(".pdf"):
            output_path += ".pdf"

        start_callback(image_files, output_path)

    def start_picture_to_pdf_conversion(
        self,
        parent,
        image_files: list,
        output_path: str,
    ) -> None:
        """Start image to PDF conversion.

        Args:
            parent: Parent widget for progress dialog
            image_files: List of image file paths to convert
            output_path: Output PDF file path
        """
        self.status_changed.emit("Converting images to PDF...", True)

        worker = ImageToPdfWorker(image_files, output_path)

        progress_dialog = QProgressDialog(
            "Initializing...", "Cancel", 0, len(image_files), parent
        )
        progress_dialog.setWindowTitle("Converting Images to PDF")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setValue(0)
        progress_dialog.setAutoClose(False)
        progress_dialog.setAutoReset(False)

        worker.progress.connect(
            lambda curr, tot, file: self._update_image_progress(
                progress_dialog, curr, tot, file
            )
        )
        worker.finished.connect(lambda res: self._image_conversion_finished(progress_dialog, res))
        progress_dialog.canceled.connect(worker.cancel)

        worker.start()

    def _update_image_progress(
        self,
        dialog: QProgressDialog,
        current: int,
        total: int,
        current_file: str,
    ) -> None:
        """Update image conversion progress dialog.

        Args:
            dialog: Progress dialog to update
            current: Current image number
            total: Total number of images
            current_file: Current image file path
        """
        dialog.setValue(current)
        dialog.setLabelText(
            f"Processing image {current} of {total}:\n{Path(current_file).name}"
        )

    def _image_conversion_finished(self, dialog: QProgressDialog, results: dict) -> None:
        """Handle image conversion completion.

        Args:
            dialog: Progress dialog to close
            results: Dictionary with conversion results
        """
        dialog.close()

        if results["success"]:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Conversion Successful")
            msg.setText("Images successfully converted to PDF!")
            msg.setInformativeText(f"PDF saved to:\n{results['output_path']}")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            self.status_changed.emit("Image conversion complete!", True)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Conversion Failed")
            msg.setText("Failed to convert images to PDF")
            msg.setInformativeText(f"Error: {results['error']}")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            self.status_changed.emit("Image conversion failed", False)

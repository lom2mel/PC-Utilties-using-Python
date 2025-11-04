from PySide6.QtCore import QThread, Signal
import pythoncom
import win32com.client
from pathlib import Path
from datetime import datetime
import shutil


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
            "converted": 0,
            "skipped": 0,
            "errors": 0,
            "error_details": [],
            "archive_folder": str(self.archive_folder),
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
                    results["converted"] += 1
                else:
                    results["skipped"] += 1
            except Exception as e:
                results["errors"] += 1
                results["error_details"].append(f"{file_path.name}: {str(e)}")

        # Move all archived files to the archive folder
        self.move_files_to_archive()

        self.finished.emit(results)

    def find_office_files(self, root_path):
        """Recursively find all Office files in the given path"""
        office_extensions = {".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"}
        office_files = []

        try:
            if root_path.is_file():
                if root_path.suffix.lower() in office_extensions:
                    office_files.append(root_path)
            else:
                for file_path in root_path.rglob("*"):
                    if (
                        file_path.is_file()
                        and file_path.suffix.lower() in office_extensions
                    ):
                        # Skip backup files
                        if not file_path.name.endswith(".backup"):
                            office_files.append(file_path)
        except PermissionError:
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
            if extension in [".doc", ".docx"]:
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
                    new_path = file_path.with_suffix(".docx")

                    self.sub_progress.emit("Saving converted file...", 75)
                    doc.SaveAs2(str(new_path.absolute()), FileFormat=12)
                    doc.Close()

                    conversion_successful = True

                    # If original was .doc, rename it to .backup and archive it
                    if extension == ".doc" and file_path != new_path:
                        self.sub_progress.emit("Creating backup...", 90)
                        backup_path = file_path.with_suffix(".doc.backup")
                        file_path.rename(backup_path)
                        self.files_to_archive.append(backup_path)

                    self.sub_progress.emit("Completed!", 100)
                    return True
                finally:
                    if word:
                        word.Quit()

            # Excel spreadsheets
            elif extension in [".xls", ".xlsx"]:
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
                    new_path = file_path.with_suffix(".xlsx")

                    self.sub_progress.emit("Saving converted file...", 75)
                    wb.SaveAs(str(new_path.absolute()), FileFormat=51)
                    wb.Close()

                    conversion_successful = True

                    # If original was .xls, rename it to .backup and archive it
                    if extension == ".xls" and file_path != new_path:
                        self.sub_progress.emit("Creating backup...", 90)
                        backup_path = file_path.with_suffix(".xls.backup")
                        file_path.rename(backup_path)
                        self.files_to_archive.append(backup_path)

                    self.sub_progress.emit("Completed!", 100)
                    return True
                finally:
                    if excel:
                        excel.Quit()

            # PowerPoint presentations
            elif extension in [".ppt", ".pptx"]:
                powerpoint = None
                try:
                    self.sub_progress.emit("Initializing Microsoft PowerPoint...", 10)
                    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
                    powerpoint.Visible = False
                    powerpoint.DisplayAlerts = False

                    # Open the presentation
                    self.sub_progress.emit(f"Opening {file_path.name}...", 25)
                    prs = powerpoint.Presentations.Open(
                        str(file_path.absolute()), WithWindow=False
                    )

                    # Save as .pptx (Office 365 format)
                    # ppSaveAsOpenXMLPresentation = 24 (pptx format)
                    self.sub_progress.emit("Converting to latest format...", 50)
                    new_path = file_path.with_suffix(".pptx")

                    self.sub_progress.emit("Saving converted file...", 75)
                    prs.SaveAs(str(new_path.absolute()), FileFormat=24)
                    prs.Close()

                    conversion_successful = True

                    # If original was .ppt, rename it to .backup and archive it
                    if extension == ".ppt" and file_path != new_path:
                        self.sub_progress.emit("Creating backup...", 90)
                        backup_path = file_path.with_suffix(".ppt.backup")
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
                        dest_path = (
                            original_dest.parent
                            / f"{original_dest.stem}_{counter}{original_dest.suffix}"
                        )
                        counter += 1

                    # Move the file
                    shutil.move(str(file_path), str(dest_path))
                except Exception:
                    # If we can't move a file, just skip it
                    pass

    def cancel(self):
        """Cancel the conversion process"""
        self.cancelled = True

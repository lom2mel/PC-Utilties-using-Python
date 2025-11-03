# PC Utilities Manager

A Windows desktop application that helps you download essential PC utilities and convert Microsoft Office files to the latest format.

## Features

- **Download Avast Antivirus**: Opens the official Avast download page
- **Scan with VirusTotal**: Opens VirusTotal for scanning files for viruses and malware
- **Download CCleaner**: Opens the official CCleaner download page
- **Office File Converter**: Convert old Office files (.doc, .xls, .ppt) to modern formats (.docx, .xlsx, .pptx)
  - Convert single files, entire folders, or whole drives
  - Automatic backup creation
  - Organized archive folder on Desktop
- **Picture to PDF Converter**: Convert images (JPG, PNG, BMP, GIF, TIFF) to PDF
  - Combine multiple images into one PDF
  - Automatic color mode conversion
  - Progress tracking

## System Requirements

- **Operating System**: Windows 10 or later
- **Python**: Python 3.8 or higher (automatically installed by auto_setup.bat)
- **Microsoft Office**: Required for the Office file converter feature (Word, Excel, PowerPoint)

## Installation Instructions

### Method 1: ONE-CLICK SETUP (Recommended - Easiest!)

**This is the simplest way to get started!**

1. **Copy the entire folder to your USB drive or target PC**
   - Make sure these files are included:
     - `download_manager.py`
     - `requirements.txt`
     - `auto_setup.bat` ← The magic one-click installer!
     - `README.md`

2. **Right-click `auto_setup.bat` and select "Run as administrator"**
   - That's it! The script will automatically:
     - ✓ Download the latest Python installer from python.org
     - ✓ Install Python with "Add to PATH" enabled
     - ✓ Install all required dependencies (PySide6, pywin32, Pillow)
     - ✓ Launch the application

**Note**: Administrator privileges are required to install Python system-wide and configure PATH.

### Method 2: Quick Install (If Python is already installed)

1. **Copy the entire folder to your USB drive or target PC**
   - Make sure these files are included:
     - `download_manager.py`
     - `requirements.txt`
     - `install.bat`
     - `run.bat`
     - `README.md`

2. **Install Python** (if not already installed)
   - Download from: https://www.python.org/downloads/
   - **IMPORTANT**: During installation, check the box "Add Python to PATH"
   - Minimum version: Python 3.8

3. **Run the installer**
   - Double-click `install.bat`
   - Wait for all dependencies to install
   - The script will install:
     - PySide6 (GUI framework)
     - pywin32 (Windows COM automation for Office conversion)
     - Pillow (Image processing for PDF conversion)

4. **Launch the application**
   - Double-click `run.bat`
   - OR run: `python download_manager.py`

### Method 3: Manual Installation

If you prefer to install manually or the batch script doesn't work:

```batch
# Install dependencies
python -m pip install -r requirements.txt

# Run the application
python download_manager.py
```

## Usage

### Downloading Utilities

1. Launch the application using `run.bat`
2. Click on any download button:
   - **Download Avast Antivirus**: Opens browser to Avast download page
   - **Scan file with VirusTotal**: Opens VirusTotal file scanner
   - **Download CCleaner**: Opens browser to CCleaner download page
3. Follow the on-screen instructions in your browser to complete downloads

### Converting Office Files

1. Click "Convert Office Files to Latest Format"
2. Choose conversion type:
   - **Select File**: Convert a single Office file
   - **Select Folder**: Convert all Office files in a folder
   - **Select Drive**: Convert all Office files on an entire drive
3. The converter will:
   - Find all Office files (.doc, .docx, .xls, .xlsx, .ppt, .pptx)
   - Convert old formats to modern Office 365 compatible formats
   - Create backups of original files
   - Move backups to an organized archive folder on your Desktop
4. After completion, check the archive folder on Desktop for backups

**Note**: Microsoft Office must be installed for the file converter to work.

### Converting Pictures to PDF

1. Click "Convert Pictures to PDF"
2. Select one or more image files:
   - Supported formats: JPG, JPEG, PNG, BMP, GIF, TIFF
   - You can select multiple images using Ctrl+Click
3. Choose where to save the output PDF file
4. The converter will:
   - Process each image and convert to PDF-compatible format
   - Combine all images into a single PDF document
   - Show progress for each image being processed
5. After completion, your PDF will be saved to the selected location

## Package Contents

```
PC Utilities Manager/
├── download_manager.py    # Main application file
├── requirements.txt       # Python dependencies
├── auto_setup.bat        # ONE-CLICK installer (downloads Python, installs everything)
├── install.bat           # Installation script (if Python already installed)
├── run.bat               # Quick launch script
└── README.md             # This file
```

## Troubleshooting

### auto_setup.bat won't run
- Make sure you right-click and select "Run as administrator"
- Check your internet connection (needed to download Python)
- Try disabling antivirus temporarily (it may block the download)

### Python not found
- Use `auto_setup.bat` which automatically installs Python
- OR manually install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during manual installation
- Try running `python --version` in Command Prompt

### Dependencies installation failed
- Make sure you have internet connection
- Try running `auto_setup.bat` as Administrator
- OR manually install: `python -m pip install PySide6 pywin32 Pillow`

### Office converter not working
- Microsoft Office must be installed on the PC
- Try running the application as Administrator
- Make sure Office is properly activated

### Picture to PDF converter not working
- Make sure Pillow is installed: `python -m pip install Pillow`
- Check that image files are in a supported format (JPG, PNG, BMP, GIF, TIFF)
- Try with a different image file

### Application won't start
- Check that all files are in the same folder
- Run `auto_setup.bat` as Administrator to reinstall everything
- Check for error messages in the Command Prompt

## Creating a Portable Version

To create a portable version for USB distribution:

1. Copy all files to your USB drive:
   - `download_manager.py`
   - `requirements.txt`
   - `auto_setup.bat`
   - `install.bat`
   - `run.bat`
   - `README.md`

2. On any target PC:
   - **Option A (Easiest)**: Right-click `auto_setup.bat` → "Run as administrator"
     - Everything installs automatically, including Python!
   - **Option B**: If Python is already installed, just run `install.bat` then `run.bat`

3. The application runs directly from the USB drive - no copying needed!

## Security Notes

- All download buttons open official vendor websites
- No files are downloaded directly by the application
- Downloads occur through your browser for security
- VirusTotal is a trusted malware scanning service

## Version

Current Version: 1.0.0

## License

This software is provided as-is for personal use.

## Support

For issues or questions:
- Check the Troubleshooting section above
- Ensure all system requirements are met
- Verify Python and Office installations

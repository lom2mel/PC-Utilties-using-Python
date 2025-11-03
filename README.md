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

## System Requirements

- **Operating System**: Windows 10 or later
- **Python**: Python 3.8 or higher
- **Microsoft Office**: Required for the Office file converter feature (Word, Excel, PowerPoint)

## Installation Instructions

### Method 1: Quick Install (Recommended)

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

4. **Launch the application**
   - Double-click `run.bat`
   - OR run: `python download_manager.py`

### Method 2: Manual Installation

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

## Package Contents

```
PC Utilities Manager/
├── download_manager.py    # Main application file
├── requirements.txt       # Python dependencies
├── setup.py              # Setup configuration
├── install.bat           # Windows installation script
├── run.bat               # Quick launch script
└── README.md             # This file
```

## Troubleshooting

### Python not found
- Make sure Python is installed and added to PATH
- Try running `python --version` in Command Prompt
- Reinstall Python and check "Add Python to PATH"

### Dependencies installation failed
- Make sure you have internet connection
- Try running `install.bat` as Administrator
- Manually install: `python -m pip install PySide6 pywin32`

### Office converter not working
- Microsoft Office must be installed on the PC
- Try running the application as Administrator
- Make sure Office is properly activated

### Application won't start
- Check that all files are in the same folder
- Run `install.bat` again to reinstall dependencies
- Check for error messages in the Command Prompt

## Creating a Portable Version

To create a portable version for USB distribution:

1. Install all dependencies on your development PC
2. Copy the entire folder to USB
3. On the target PC, just run `install.bat` to set up dependencies
4. The application will work without needing to copy files to the target PC

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

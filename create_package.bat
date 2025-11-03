@echo off
echo ===============================================
echo PC Utilities Manager - Package Creator
echo ===============================================
echo.
echo This script will create a portable package
echo that you can copy to a USB drive.
echo.

REM Set the package name
set PACKAGE_NAME=PC_Utilities_Manager_Portable
set OUTPUT_DIR=%USERPROFILE%\Desktop\%PACKAGE_NAME%

echo Creating package directory...
if exist "%OUTPUT_DIR%" (
    echo Removing existing package...
    rmdir /s /q "%OUTPUT_DIR%"
)

mkdir "%OUTPUT_DIR%"

echo.
echo Copying files to package...
echo.

REM Copy all necessary files
copy /Y "download_manager.py" "%OUTPUT_DIR%\" >nul
copy /Y "requirements.txt" "%OUTPUT_DIR%\" >nul
copy /Y "setup.py" "%OUTPUT_DIR%\" >nul
copy /Y "install.bat" "%OUTPUT_DIR%\" >nul
copy /Y "run.bat" "%OUTPUT_DIR%\" >nul
copy /Y "README.md" "%OUTPUT_DIR%\" >nul

echo Files copied:
echo   - download_manager.py
echo   - requirements.txt
echo   - setup.py
echo   - install.bat
echo   - run.bat
echo   - README.md
echo.

REM Create a quick start guide
echo Creating QUICK_START.txt...
(
echo ====================================================
echo PC UTILITIES MANAGER - QUICK START GUIDE
echo ====================================================
echo.
echo STEP 1: Install Python
echo    - Go to https://www.python.org/downloads/
echo    - Download Python 3.8 or higher
echo    - IMPORTANT: Check "Add Python to PATH" during install
echo.
echo STEP 2: Install Dependencies
echo    - Double-click "install.bat"
echo    - Wait for installation to complete
echo.
echo STEP 3: Run the Application
echo    - Double-click "run.bat"
echo.
echo ====================================================
echo.
echo FEATURES:
echo    - Download Avast Antivirus
echo    - Scan files with VirusTotal
echo    - Download CCleaner
echo    - Convert Office files to latest format
echo.
echo REQUIREMENTS:
echo    - Windows 10 or later
echo    - Python 3.8 or higher
echo    - Microsoft Office ^(for file converter^)
echo.
echo For detailed instructions, see README.md
echo ====================================================
) > "%OUTPUT_DIR%\QUICK_START.txt"

echo.
echo ===============================================
echo Package created successfully!
echo ===============================================
echo.
echo Location: %OUTPUT_DIR%
echo.
echo You can now:
echo   1. Copy this folder to a USB drive
echo   2. Transfer to any Windows PC
echo   3. Follow the instructions in QUICK_START.txt
echo.
echo Opening package folder...
explorer "%OUTPUT_DIR%"
echo.
pause

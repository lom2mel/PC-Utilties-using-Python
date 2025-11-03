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
copy /Y "auto_setup.bat" "%OUTPUT_DIR%\" >nul
copy /Y "install.bat" "%OUTPUT_DIR%\" >nul
copy /Y "install_simple.bat" "%OUTPUT_DIR%\" >nul
copy /Y "run.bat" "%OUTPUT_DIR%\" >nul
copy /Y "README.md" "%OUTPUT_DIR%\" >nul

echo Files copied:
echo   - download_manager.py
echo   - requirements.txt
echo   - auto_setup.bat (ONE-CLICK INSTALLER)
echo   - install.bat
echo   - install_simple.bat
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
echo ONE-CLICK INSTALLATION ^(EASIEST METHOD^):
echo.
echo    1. Right-click "auto_setup.bat"
echo    2. Select "Run as administrator"
echo    3. Done! Everything installs automatically!
echo.
echo The auto_setup.bat will:
echo    - Download and install Python automatically
echo    - Add Python to PATH
echo    - Install all dependencies
echo    - Create Desktop shortcut
echo    - Create Start Menu shortcut
echo    - Launch the application
echo.
echo ====================================================
echo.
echo MANUAL INSTALLATION ^(If Python already installed^):
echo.
echo STEP 1: Install Dependencies
echo    - Double-click "install.bat"
echo    - Wait for installation to complete
echo.
echo STEP 2: Run the Application
echo    - Double-click "run.bat"
echo.
echo ====================================================
echo.
echo FEATURES:
echo    - Download Avast Antivirus
echo    - Scan files with VirusTotal
echo    - Download CCleaner
echo    - Convert Office files to latest format
echo    - Convert pictures to PDF
echo.
echo REQUIREMENTS:
echo    - Windows 10 or later
echo    - Internet connection ^(for auto_setup.bat^)
echo    - Microsoft Office ^(for Office file converter^)
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

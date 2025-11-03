@echo off
echo ===============================================
echo PC Utilities Manager - Installation Script
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python detected. Checking version...
python --version
echo.

REM Check if pip is available
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo Installing dependencies...
echo.

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
echo.

REM Install required packages one by one for better error handling
echo Installing PySide6...
python -m pip install PySide6>=6.5.0
if %errorlevel% neq 0 (
    echo Warning: Failed to install PySide6>=6.5.0, trying lower version...
    python -m pip install PySide6
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PySide6
        pause
        exit /b 1
    )
)

echo Installing pywin32...
python -m pip install pywin32>=305
if %errorlevel% neq 0 (
    echo Warning: Failed to install pywin32>=305, trying lower version...
    python -m pip install pywin32
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install pywin32
        pause
        exit /b 1
    )
)

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ===============================================
echo Installation completed successfully!
echo ===============================================
echo.
echo To run the application:
echo   1. Double-click run.bat
echo   OR
echo   2. Run: python download_manager.py
echo.
pause

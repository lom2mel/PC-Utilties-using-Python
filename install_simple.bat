@echo off
:: Change to the directory where this batch file is located
cd /d "%~dp0"

echo ===============================================
echo PC Utilities Manager - Simple Installation
echo ===============================================
echo.

REM Check Python version
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo Step 1: Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Step 2: Installing PySide6 (GUI library)...
python -m pip install PySide6

echo.
echo Step 3: Installing pywin32 (Windows utilities)...
python -m pip install pywin32

echo.
echo Step 4: Installing Pillow (Image processing)...
python -m pip install Pillow

echo.
echo ===============================================
echo Installation Complete!
echo ===============================================
echo.
echo To run the application:
echo   Double-click run.bat
echo.
pause

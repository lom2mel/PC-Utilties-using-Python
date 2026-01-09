@echo off
REM Fix Virtual Environment Script for PC Utilities Manager
REM This script sets up a working virtual environment outside of OneDrive

setlocal enabledelayedexpansion

echo PC Utilities Manager - Virtual Environment Setup
echo ================================================
echo.

REM Get the project directory
set "PROJECT_DIR=%~dp0"

REM Define a path outside OneDrive for the venv
set "VENV_PATH=%USERPROFILE%\.venvs\pc-utilities-manager"

REM Check if venv already exists
if exist "%VENV_PATH%" (
    echo Found existing virtual environment at: %VENV_PATH%
    set /p CHOICE="Do you want to recreate it? (y/N): "
    if /i "!CHOICE!"=="y" (
        echo Removing old virtual environment...
        rmdir /s /q "%VENV_PATH%"
    ) else (
        echo Using existing virtual environment
    )
)

REM Create virtual environment if it doesn't exist
if not exist "%VENV_PATH%" (
    echo Creating new virtual environment at: %VENV_PATH%
    python -m venv "%VENV_PATH%"

    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate the virtual environment
echo.
echo Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"

REM Install dependencies
echo.
echo Installing dependencies...
echo.

REM Try UV first
set UV_LINK_MODE=copy
uv sync --link-mode=copy

if errorlevel 1 (
    echo.
    echo WARNING: UV sync had issues. Trying alternative installation...
    echo Installing PySide6 with pip...
    python -m pip install --upgrade pip
    python -m pip install PySide6
)

echo.
echo ================================================
echo Setup complete!
echo.
echo Virtual environment location: %VENV_PATH%
echo Project location: %PROJECT_DIR%
echo.
echo To activate this environment in the future, run:
echo   call "%VENV_PATH%\Scripts\activate.bat"
echo.
echo Then run the application:
echo   python main.py
echo.

pause

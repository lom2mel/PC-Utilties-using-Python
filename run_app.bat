@echo off
REM PC Utilities Manager - Run Application
REM This script activates the virtual environment and runs the app

setlocal enabledelayedexpansion

REM Define venv path (outside OneDrive)
set "VENV_PATH=%USERPROFILE%\.venvs\pc-utilities-manager"

REM Check if venv exists
if not exist "%VENV_PATH%\Scripts\activate.bat" (
    echo Virtual environment not found at: %VENV_PATH%
    echo Creating virtual environment...
    python -m venv "%VENV_PATH%"

    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo.
        echo Make sure Python is installed and in your PATH
        pause
        exit /b 1
    )

    echo.
    echo Installing dependencies...
    call "%VENV_PATH%\Scripts\activate.bat"
    python -m pip install --upgrade pip
    pip install PySide6 pydantic pydantic-settings requests structlog

    if errorlevel 1 (
        echo WARNING: Some packages failed to install
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"

REM Run the application
echo.
echo Starting PC Utilities Manager...
echo.
python main.py

REM If app crashes, keep window open
if errorlevel 1 (
    echo.
    echo Application exited with error code: %errorlevel%
    echo.
    pause
)

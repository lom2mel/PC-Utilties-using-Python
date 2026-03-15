@echo off
REM PC Utilities Manager Launcher (Debug Mode)
REM This script runs the app with console output visible for debugging

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    uv venv
    echo Installing dependencies...
    uv pip install -e .
)

echo Starting PC Utilities Manager in debug mode...
echo Press Ctrl+C to stop the debugger.
echo.

REM Run with console visible for debugging
.venv\Scripts\python.exe src\main.py

pause

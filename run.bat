@echo off
REM PC Utilities Manager Launcher
REM This script activates the virtual environment and runs the application

REM Change to script directory
cd /d "%~dp0"

REM Check if venv exists, create if not
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    uv venv
    echo Installing dependencies...
    uv pip install -e .
)

REM Run the application
.venv\Scripts\python.exe src\main.py

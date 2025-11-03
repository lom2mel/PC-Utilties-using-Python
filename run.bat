@echo off
echo Starting PC Utilities Manager...
python download_manager.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to run the application
    echo Make sure you have run install.bat first
    pause
)

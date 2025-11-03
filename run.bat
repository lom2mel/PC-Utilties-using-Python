@echo off
:: Change to the directory where this batch file is located
cd /d "%~dp0"

echo Starting PC Utilities Manager...
start "" pythonw download_manager.py
exit

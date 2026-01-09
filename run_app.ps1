# PC Utilities Manager - Run Application
# This script activates the virtual environment and runs the app

$ErrorActionPreference = "Stop"

# Define venv path (outside OneDrive)
$venvPath = "$env:USERPROFILE\.venvs\pc-utilities-manager"

# Check if venv exists
if (-not (Test-Path "$venvPath\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found at: $venvPath" -ForegroundColor Yellow
    Write-Host "Creating virtual environment..." -ForegroundColor Green

    python -m venv $venvPath

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        Write-Host "Make sure Python is installed and in your PATH" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }

    Write-Host ""
    Write-Host "Installing dependencies..." -ForegroundColor Green

    & "$venvPath\Scripts\Activate.ps1"
    python -m pip install --upgrade pip
    pip install PySide6 pydantic pydantic-settings requests structlog

    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Some packages failed to install" -ForegroundColor Yellow
    }
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& "$venvPath\Scripts\Activate.ps1"

# Run the application
Write-Host ""
Write-Host "Starting PC Utilities Manager..." -ForegroundColor Cyan
Write-Host ""

try {
    python main.py
}
catch {
    Write-Host ""
    Write-Host "Application exited with error: $_" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

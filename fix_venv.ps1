# Fix Virtual Environment Script
# This script helps set up a working virtual environment outside of OneDrive

# Get the project directory
$projectDir = $PSScriptRoot

# Define a path outside OneDrive for the venv
$venvPath = "$env:USERPROFILE\.venvs\pc-utilities-manager"

Write-Host "PC Utilities Manager - Virtual Environment Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv already exists
if (Test-Path $venvPath) {
    Write-Host "Found existing virtual environment at: $venvPath" -ForegroundColor Yellow
    $choice = Read-Host "Do you want to recreate it? (y/N)"
    if ($choice -eq 'y' -or $choice -eq 'Y') {
        Write-Host "Removing old virtual environment..." -ForegroundColor Yellow
        Remove-Item -Path $venvPath -Recurse -Force
    } else {
        Write-Host "Using existing virtual environment" -ForegroundColor Green
    }
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating new virtual environment at: $venvPath" -ForegroundColor Green
    python -m venv $venvPath

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate the virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Green
& "$venvPath\Scripts\Activate.ps1"

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies with UV (this may take a while)..." -ForegroundColor Green
Write-Host "Note: Using --link-mode=copy for OneDrive compatibility" -ForegroundColor Yellow

# Set UV to use copy mode for OneDrive compatibility
$env:UV_LINK_MODE = "copy"
uv sync --link-mode=copy

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "WARNING: UV sync had issues. Trying alternative installation..." -ForegroundColor Yellow
    Write-Host "Installing PySide6 with pip..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    python -m pip install PySide6
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Virtual environment location: $venvPath" -ForegroundColor Cyan
Write-Host "Project location: $projectDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "To activate this environment in the future, run:" -ForegroundColor Yellow
Write-Host "  & `"$venvPath\Scripts\Activate.ps1`"" -ForegroundColor White
Write-Host ""
Write-Host "Then run the application:" -ForegroundColor Yellow
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""

# Keep the shell open
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

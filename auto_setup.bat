@echo off
setlocal enabledelayedexpansion

:: Check for administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ===============================================
    echo Administrator privileges required
    echo ===============================================
    echo This script needs administrator rights to:
    echo - Install Python system-wide
    echo - Add Python to PATH
    echo - Install dependencies
    echo.
    echo Please right-click this file and select "Run as administrator"
    pause
    exit /b 1
)

echo ===============================================
echo PC Utilities Manager - Auto Setup
echo One-Click Installation
echo ===============================================
echo.

:: Set variables
set "PYTHON_VERSION=3.13.1"
set "PYTHON_MAJOR=3.13"
set "DOWNLOAD_DIR=%TEMP%\python_installer"
set "PYTHON_INSTALLER=%DOWNLOAD_DIR%\python_installer.exe"

:: Create download directory
if not exist "%DOWNLOAD_DIR%" mkdir "%DOWNLOAD_DIR%"

:: Check if Python is already installed and in PATH
echo [STEP 1/4] Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is already installed:
    python --version
    echo.
    goto :install_dependencies
)

echo Python not found. Proceeding with automatic installation...
echo.

:: Get latest Python version from python.org
echo [STEP 2/4] Downloading latest Python installer...
echo.
echo Fetching latest Python version information...

:: Use PowerShell to get the latest version
for /f "tokens=*" %%a in ('powershell -command "try { $response = Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/' -UseBasicParsing; $links = $response.Links | Where-Object { $_.href -match '^\d+\.\d+\.\d+/$' } | Select-Object -ExpandProperty href; $versions = $links | ForEach-Object { $_ -replace '/','' } | Sort-Object { [version]$_ } -Descending; $versions[0] } catch { '3.13.1' }"') do set "PYTHON_VERSION=%%a"

echo Latest Python version: %PYTHON_VERSION%
echo.

:: Determine architecture
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    set "PYTHON_ARCH=amd64"
    set "INSTALLER_NAME=python-%PYTHON_VERSION%-amd64.exe"
) else (
    set "PYTHON_ARCH=win32"
    set "INSTALLER_NAME=python-%PYTHON_VERSION%.exe"
)

:: Construct download URL
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%INSTALLER_NAME%"

echo Downloading from: %PYTHON_URL%
echo Please wait, this may take a few minutes...
echo.

:: Download Python installer using PowerShell
powershell -command "& { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $ProgressPreference = 'SilentlyContinue'; try { Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'; Write-Host 'Download completed successfully!' } catch { Write-Host 'Download failed. Trying alternative version...'; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.13.1/python-3.13.1-amd64.exe' -OutFile '%PYTHON_INSTALLER%' } }"

if not exist "%PYTHON_INSTALLER%" (
    echo ERROR: Failed to download Python installer
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo [STEP 3/4] Installing Python with PATH enabled...
echo This may take several minutes. Please wait...
echo.

:: Install Python silently with all features and add to PATH
:: InstallAllUsers=1 - Install for all users
:: PrependPath=1 - Add Python to PATH
:: Include_test=0 - Don't include tests
:: Include_pip=1 - Include pip
:: Include_launcher=1 - Include py launcher

"%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1 Include_launcher=1 Include_tcltk=1 Include_doc=0 Include_dev=0 AssociateFiles=1 Shortcuts=1

:: Wait for installation to complete
timeout /t 5 /nobreak >nul

:: Refresh environment variables
echo Refreshing environment variables...
call :RefreshEnv

:: Verify Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python installation completed but python is not in PATH
    echo Please restart your computer and run this script again.
    pause
    exit /b 1
)

echo.
echo Python installed successfully:
python --version
echo.

:install_dependencies
echo [STEP 4/4] Installing Python dependencies...
echo.

:: Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel --quiet

:: Install Pillow for image to PDF conversion
echo Installing Pillow for image processing...
python -m pip install Pillow --quiet
if %errorlevel% neq 0 (
    echo Warning: Failed to install Pillow
)

:: Install PySide6
echo Installing PySide6 (GUI framework)...
python -m pip install PySide6>=6.5.0 --quiet
if %errorlevel% neq 0 (
    echo Retrying with default version...
    python -m pip install PySide6 --quiet
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PySide6
        pause
        exit /b 1
    )
)

:: Install pywin32
echo Installing pywin32 (Windows COM automation)...
python -m pip install pywin32>=305 --quiet
if %errorlevel% neq 0 (
    echo Retrying with default version...
    python -m pip install pywin32 --quiet
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install pywin32
        pause
        exit /b 1
    )
)

echo.
echo ===============================================
echo Installation completed successfully!
echo ===============================================
echo.
echo All components installed:
echo   - Python %PYTHON_VERSION%
echo   - PySide6 (GUI framework)
echo   - pywin32 (Windows automation)
echo   - Pillow (Image processing)
echo.

:: Clean up installer
if exist "%PYTHON_INSTALLER%" del /f /q "%PYTHON_INSTALLER%"
if exist "%DOWNLOAD_DIR%" rmdir /q "%DOWNLOAD_DIR%"

:: Create shortcuts
echo Creating shortcuts...
echo.

:: Get the full path to the script directory
set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%download_manager.py"
set "RUN_BAT=%SCRIPT_DIR%run.bat"

:: Create Desktop shortcut using PowerShell
echo Creating Desktop shortcut...
powershell -command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\PC Utilities Manager.lnk'); $Shortcut.TargetPath = '%RUN_BAT%'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.IconLocation = 'shell32.dll,162'; $Shortcut.Description = 'PC Utilities Manager - Download utilities and convert files'; $Shortcut.Save()"

:: Create Start Menu shortcut
echo Creating Start Menu shortcut...
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
if not exist "%START_MENU%\PC Utilities" mkdir "%START_MENU%\PC Utilities"
powershell -command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\PC Utilities\PC Utilities Manager.lnk'); $Shortcut.TargetPath = '%RUN_BAT%'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.IconLocation = 'shell32.dll,162'; $Shortcut.Description = 'PC Utilities Manager - Download utilities and convert files'; $Shortcut.Save()"

:: Create uninstall shortcut in Start Menu
echo Creating uninstall shortcut...
(
echo @echo off
echo echo ================================================
echo echo PC Utilities Manager - Uninstaller
echo echo ================================================
echo echo.
echo echo This will remove:
echo echo   - Desktop shortcut
echo echo   - Start Menu shortcuts
echo echo.
echo echo Python and dependencies will NOT be removed.
echo echo.
echo pause
echo.
echo if exist "%USERPROFILE%\Desktop\PC Utilities Manager.lnk" del "%USERPROFILE%\Desktop\PC Utilities Manager.lnk"
echo if exist "%START_MENU%\PC Utilities" rmdir /s /q "%START_MENU%\PC Utilities"
echo.
echo echo Uninstall complete!
echo pause
) > "%SCRIPT_DIR%uninstall.bat"

powershell -command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\PC Utilities\Uninstall PC Utilities Manager.lnk'); $Shortcut.TargetPath = '%SCRIPT_DIR%uninstall.bat'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.IconLocation = 'shell32.dll,131'; $Shortcut.Description = 'Uninstall PC Utilities Manager'; $Shortcut.Save()"

echo.
echo ===============================================
echo Setup Complete!
echo ===============================================
echo.
echo Shortcuts created:
echo   - Desktop: PC Utilities Manager
echo   - Start Menu: PC Utilities Manager
echo.
echo Starting PC Utilities Manager...
echo.
timeout /t 2 /nobreak >nul

:: Launch the application
start "" "%RUN_BAT%"

echo.
echo The application is now running!
echo You can close this window.
echo.
timeout /t 3 /nobreak >nul

exit /b 0

:: Function to refresh environment variables
:RefreshEnv
:: Refresh PATH from registry
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "SYS_PATH=%%b"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%b"
set "PATH=%SYS_PATH%;%USER_PATH%"
goto :eof

@echo off
echo Installing PowerShell 7...
winget install --id Microsoft.Powershell --source winget --silent --accept-package-agreements --accept-source-agreements

echo.
echo Refreshing environment...
refreshenv 2>nul || call :RefreshEnv

echo.
echo Installing Context7 MCP server...
npx -y @smithery/cli install @upstash/context7-mcp --client claude

echo.
echo Installation complete!
pause
goto :eof

:RefreshEnv
echo Updating PATH...
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "SysPath=%%b"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "UserPath=%%b"
set "PATH=%SysPath%;%UserPath%"
goto :eof

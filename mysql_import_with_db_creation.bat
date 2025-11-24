@echo off
REM MySQL Database Import Script with Auto-Creation
REM This script creates databases before importing dump files

setlocal enabledelayedexpansion

echo ========================================
echo MySQL Database Import Script
echo ========================================
echo.

REM Configuration
set MYSQL_USER=root
set MYSQL_HOST=localhost
set MYSQL_PORT=3306
set DUMP_DIR=C:\Users\Lomel\OneDrive - MSFT\Documents\dumps\dumps_110225

REM Prompt for MySQL password
set /p MYSQL_PASS=Enter MySQL root password: 

echo.
echo Scanning dump directory: %DUMP_DIR%
echo.

REM Find all SQL dump files and extract database names
for %%f in ("%DUMP_DIR%\*.sql") do (
    set "filename=%%~nf"
    
    REM Extract database name (everything before first underscore or entire name)
    for /f "tokens=1 delims=_" %%d in ("!filename!") do (
        set "dbname=%%d"
        
        REM Check if we've already processed this database
        if not defined processed_!dbname! (
            echo [INFO] Processing database: !dbname!
            
            REM Create database if it doesn't exist
            echo [STEP] Creating database !dbname! if not exists...
            mysql.exe --host=%MYSQL_HOST% --user=%MYSQL_USER% --password=%MYSQL_PASS% --port=%MYSQL_PORT% -e "CREATE DATABASE IF NOT EXISTS !dbname! CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            
            if !errorlevel! equ 0 (
                echo [SUCCESS] Database !dbname! ready
                set "processed_!dbname!=1"
            ) else (
                echo [ERROR] Failed to create database !dbname!
            )
            echo.
        )
    )
)

echo.
echo ========================================
echo Database creation complete!
echo ========================================
echo.
echo You can now import your dump files.
echo Example:
echo mysql.exe -u %MYSQL_USER% -p provincial_gov_dbase ^< "%DUMP_DIR%\provincial_gov_dbase_template_sync_history.sql"
echo.
echo Or use MySQL Workbench to import the dumps.
echo.

pause

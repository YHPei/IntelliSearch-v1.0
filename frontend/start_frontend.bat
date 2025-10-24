@echo off
chcp 65001 >nul
cls
REM ============================================================================
REM AI Search Engine - Frontend Startup Script (Windows)
REM ============================================================================
REM This script handles automatic setup, dependency installation, and dev server
REM startup with robust error handling. Can be run from anywhere.
REM ============================================================================

echo ==========================================
echo AI Search Engine - Frontend Starting
echo ==========================================
echo.

REM Force change to script's directory (frontend folder)
cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM [1/4] Check package.json exists
echo [1/4] Checking package.json...
if not exist "package.json" (
    echo ERROR: package.json not found!
    echo Please ensure this script is in the frontend folder.
    echo.
    pause
    exit /b 1
)
echo [OK] package.json found
echo.

REM [2/4] Check Node.js version
echo [2/4] Checking Node.js...
node --version 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js not found!
    echo Please install Node.js from https://nodejs.org/
    echo.
    pause
    exit /b 1
)
echo [OK] Node.js found
echo.

REM [3/4] Check npm version
echo [3/4] Checking npm...
call npm --version 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm not found!
    echo Please ensure Node.js is correctly installed.
    echo.
    pause
    exit /b 1
)
echo [OK] npm found
echo.

REM [4/4] Check node_modules
echo [4/4] Checking dependencies...
if not exist "node_modules" (
    echo Dependencies not found, installing...
    echo This may take a few minutes, please wait...
    echo.
    call npm install --loglevel=error
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ERROR: npm install failed
        echo Trying with domestic mirror...
        call npm install --registry=https://registry.npmmirror.com --loglevel=error
        if %ERRORLEVEL% NEQ 0 (
            echo.
            echo ERROR: Installation failed even with mirror
            echo Please check your network connection
            echo.
            pause
            exit /b 1
        )
    )
    echo.
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already exist
)
echo.

REM Start frontend development server
echo ==========================================
echo Starting frontend development server...
echo.
echo App URL: http://localhost:5173
echo.
echo The browser should open automatically.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

call npm run dev

REM If server exits, show message and pause
echo.
echo ==========================================
echo Frontend server stopped
echo ==========================================
echo.
pause

@echo off
chcp 65001 >nul
cls
REM ============================================================================
REM AI Search Engine - Backend Startup Script (Windows)
REM ============================================================================
REM This script handles automatic setup, dependency checks, and server startup
REM with robust error handling. Can be run from anywhere.
REM ============================================================================

echo ==========================================
echo AI Search Engine - Backend Starting
echo ==========================================
echo.

REM Force change to script's directory (backend folder)
cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM [1/5] Check main.py exists
echo [1/5] Checking main.py...
if not exist "main.py" (
    echo ERROR: main.py not found!
    echo Please ensure this script is in the backend folder.
    echo.
    pause
    exit /b 1
)
echo [OK] main.py found
echo.

REM [2/5] Check Python version
echo [2/5] Checking Python...
python --version 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM [3/5] Check virtual environment
echo [3/5] Checking virtual environment...
if not exist "venv\Scripts\python.exe" (
    echo Virtual environment not found, creating...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to create virtual environment
        echo.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)
echo.

REM [4/5] Check dependencies
echo [4/5] Installing/checking dependencies...
if exist "requirements.txt" (
    call venv\Scripts\pip.exe install -q -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo WARNING: Some dependencies may have failed to install
        echo The server will try to start anyway...
    ) else (
        echo [OK] Dependencies installed
    )
) else (
    echo WARNING: requirements.txt not found
)
echo.

REM [5/5] Check .env file
echo [5/5] Checking configuration...
if exist ".env" (
    echo [OK] .env file found
    goto :config_done
)

REM .env doesn't exist, need to create it
echo WARNING: .env file not found
if not exist "env.example" (
    echo.
    echo ERROR: env.example not found
    echo Please create a .env file manually
    echo.
    pause
    exit /b 1
)

REM Create .env from env.example
echo Copying from env.example...
copy env.example .env >nul
echo.
echo [IMPORTANT] .env file created!
echo.
echo You need to add your API keys:
echo   - SEARCHCANS_API_KEY (Required)
echo   - OPENAI_API_KEY or DASHSCOPE_API_KEY (Optional)
echo.
echo Press any key to open .env in editor, or close this window to edit manually later.
pause >nul
notepad .env
echo.
echo [OK] Configuration file ready
echo.

:config_done
echo.

REM Start backend service
echo ==========================================
echo Starting backend service...
echo.
echo API URL:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

REM Use full path to avoid any issues
"%~dp0venv\Scripts\python.exe" "%~dp0main.py"

REM If server exits, show message and pause
echo.
echo ==========================================
echo Backend server stopped
echo ==========================================
echo.
pause

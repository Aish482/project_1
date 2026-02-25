@echo off
REM Smart Logistics Platform - Windows Launch Script
REM This script sets up the environment and runs the Streamlit app

echo.
echo ================================================================================
echo  Smart Logistics Management ^& Analytics Platform
echo  Streamlit Dashboard Launch Script (Windows)
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo [✓] Python is installed
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [*] Creating virtual environment...
    python -m venv venv
    echo [✓] Virtual environment created
    echo.
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
echo [✓] Virtual environment activated
echo.

REM Install/upgrade requirements
echo [*] Installing dependencies...
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo [✓] Dependencies installed
echo.

REM Run setup if needed
if "%1"=="--setup" (
    echo [*] Running setup wizard...
    python setup.py --all
    echo.
)

REM Run the Streamlit app
echo [*] Starting Streamlit application...
echo.
echo ================================================================================
echo  Dashboard will open in your default browser at: http://localhost:8501
echo  Press CTRL+C to stop the server
echo ================================================================================
echo.

streamlit run app.py

pause

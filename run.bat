@echo off
echo ========================================
echo   Web3 MarketMind 4.0 - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo.

REM Create necessary directories
if not exist "models\" mkdir models
if not exist "data\" mkdir data
echo.

REM Run the application
echo ========================================
echo   Starting Web3 MarketMind 4.0...
echo ========================================
echo.
echo   Access the app at: http://localhost:8501
echo   Demo credentials: demo / demo123
echo.
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

streamlit run app_v4.py

pause

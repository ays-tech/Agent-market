@echo off
echo ========================================
echo   Agent Market - Starting Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting Agent Market...
echo The app will open in your browser automatically.
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

streamlit run app.py

pause


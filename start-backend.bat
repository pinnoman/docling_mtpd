@echo off
echo Starting Docling Backend Server...
echo.

cd backend

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if dependencies are installed
pip show docling >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

echo Backend server starting on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python main.py

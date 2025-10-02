@echo off
echo ========================================
echo Starting Docling Application
echo ========================================
echo.

REM Start backend in a new window
echo Starting Backend Server...
start "Docling Backend" cmd /k "%~dp0start-backend.bat"

REM Wait a few seconds for backend to initialize
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Start frontend in a new window
echo Starting Frontend...
start "Docling Frontend" cmd /k "%~dp0start-frontend.bat"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Two new windows will open for each server.
echo Close those windows to stop the servers.
echo ========================================
pause

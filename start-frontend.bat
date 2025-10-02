@echo off
echo Starting Docling Frontend...
echo.

cd docling-ui

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Installing dependencies...
    call npm install
    echo.
)

echo Frontend starting on http://localhost:3000
echo Press Ctrl+C to stop the server
echo.
call npm run dev

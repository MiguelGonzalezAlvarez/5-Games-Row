@echo off
echo ========================================
echo Starting 5 Games in a Row Development Servers
echo ========================================
echo.

echo [1/2] Starting Backend Server on port 8002...
cd /d "%~dp0backend"
start "Backend - 5 Games Row" cmd /k "python main.py"

echo [2/2] Starting Frontend Server...
cd /d "%~dp0frontend"
start "Frontend - 5 Games Row" cmd /k "npm run dev"

echo.
echo ========================================
echo Servers starting...
echo.
echo Backend: http://localhost:8002
echo Frontend: http://localhost:4321 (or next available port)
echo.
echo Press any key to exit this window (servers will keep running)
echo ========================================
pause >nul

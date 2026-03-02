@echo off
echo Starting Backend Server...
cd /d "%~dp0backend"
start "Backend" cmd /k "python -m uvicorn main:app --host 127.0.0.1 --port 8002"

echo Starting Frontend Server...
cd /d "%~dp0frontend"
start "Frontend" cmd /k "npm run dev"

echo.
echo Servers are starting...
echo Backend: http://localhost:8002
echo Frontend: http://localhost:4321 (or next available port)
echo.
pause

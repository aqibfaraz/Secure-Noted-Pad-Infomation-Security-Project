@echo off
REM Secure Notepad - Complete Startup Script for Windows

echo.
echo ====================================
echo  Secure Notepad Application Startup
echo ====================================
echo.

REM Check Node.js
echo Checking Node.js installation...
node --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    exit /b 1
)
echo Node.js: OK

REM Check Python
echo Checking Python installation...
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/
    exit /b 1
)
echo Python: OK

REM Backend Setup
echo.
echo Setting up Backend...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment and installing packages...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet

echo Starting Flask server on port 5000...
start cmd /k "cd %cd% && venv\Scripts\activate.bat && python app.py"
echo Backend started (check the new window)

REM Frontend Setup
echo.
echo Setting up Frontend...
cd ..\frontend

echo Installing npm packages...
call npm install --quiet

echo Starting Vite dev server on port 3000...
start cmd /k "cd %cd% && npm run dev"
echo Frontend starting (check the new window)

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Open http://localhost:3000 in your browser
echo.
pause

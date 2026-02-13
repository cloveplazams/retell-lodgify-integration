@echo off
echo Starting Retell-Lodgify Web App...

:: Check for Python (try 'python' first, then 'py')
set PYTHON_CMD=python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Python is not installed or not in your PATH.
        echo Please install Python from https://www.python.org/downloads/
        echo IMPORTANT: Check "Add Python to PATH" during installation.
        pause
        exit /b
    )
    set PYTHON_CMD=py
)

echo Using Python command: %PYTHON_CMD%
echo Installing dependencies (Flask, SQLAlchemy)...
%PYTHON_CMD% -m pip install -r requirements.txt

echo.
echo ========================================================
echo       Retell-Lodgify Manager is RUNNING
echo ========================================================
echo.
echo 1. Open your browser and go to: http://localhost:5000
echo    (This is your Dashboard to add/edit properties)
echo.
echo 2. Make sure ngrok is running in a separate window:
echo    ngrok http 5000
echo.
echo 3. The server logs will appear below...
echo.

%PYTHON_CMD% app.py
pause

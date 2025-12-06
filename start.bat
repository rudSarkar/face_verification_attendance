@echo off
REM Face Recognition Attendance System - Startup Script for Windows

echo ==========================================
echo Face Recognition Attendance System
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [*] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\.requirements_installed" (
    echo [*] Installing dependencies...
    pip install -r requirements.txt
    type nul > venv\.requirements_installed
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

echo.

REM Check if database exists
if not exist "attendance_system.db" (
    echo [*] Initializing database...
    python database.py
    echo [OK] Database initialized
) else (
    echo [OK] Database already exists
)

echo.
echo ==========================================
echo Starting Flask Application...
echo ==========================================
echo.
echo Access the application at:
echo   Home: http://localhost:8181
echo   Admin: http://localhost:8181/admin/login
echo   Mark Attendance: http://localhost:8181/mark-attendance
echo.
echo Default Admin Credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

REM Start Flask application
python app.py

pause

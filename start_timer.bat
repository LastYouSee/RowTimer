@echo off
echo Starting Rowing Timer Application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.6 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if the main application file exists
if not exist "rowing_timer.py" (
    echo Error: rowing_timer.py not found
    echo Make sure you're running this from the correct directory
    pause
    exit /b 1
)

REM Try to run the application with sample data option first
if exist "start_with_sample.py" (
    echo Running with sample data option...
    python start_with_sample.py
) else (
    REM Fallback to regular application
    echo Running basic application...
    python rowing_timer.py
)

REM Check if there was an error
if %errorlevel% neq 0 (
    echo.
    echo An error occurred while running the application.
    echo Press any key to exit...
    pause >nul
)

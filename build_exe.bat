@echo off
echo ========================================
echo   SKELSKØR ROKLUB - BUILD EXECUTABLE
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if we're in the correct directory
if not exist "rowing_timer.py" (
    echo ERROR: rowing_timer.py not found
    echo Please run this from the RowTimer directory
    pause
    exit /b 1
)

echo Installing PyInstaller if needed...
python -m pip install pyinstaller

echo.
echo Installing ReportLab for PDF support...
python -m pip install reportlab

echo.
echo ========================================
echo   BUILDING EXECUTABLE...
echo ========================================

REM Build the executable
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "SkelskørRoklub_Timer" ^
    --distpath "dist" ^
    --workpath "build" ^
    --add-data "club_logo.txt;." ^
    --add-data "README.md;." ^
    --add-data "USER_GUIDE.md;." ^
    --hidden-import "tkinter" ^
    --hidden-import "tkinter.ttk" ^
    --hidden-import "tkinter.filedialog" ^
    --hidden-import "tkinter.messagebox" ^
    --hidden-import "reportlab.platypus" ^
    --hidden-import "reportlab.lib.pagesizes" ^
    --hidden-import "reportlab.lib.styles" ^
    --hidden-import "reportlab.lib.colors" ^
    --exclude-module "matplotlib" ^
    --exclude-module "numpy" ^
    --exclude-module "pandas" ^
    rowing_timer.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo   BUILD COMPLETED SUCCESSFULLY!
echo ========================================

if exist "dist\SkelskørRoklub_Timer.exe" (
    for %%A in ("dist\SkelskørRoklub_Timer.exe") do set size=%%~zA
    set /a size_mb=!size! / 1024 / 1024
    echo Executable: dist\SkelskørRoklub_Timer.exe
    echo Size: !size_mb! MB
    echo.
    echo The executable is ready for distribution!
    echo Double-click SkelskørRoklub_Timer.exe to run
) else (
    echo ERROR: Executable not found after build
)

echo.
pause

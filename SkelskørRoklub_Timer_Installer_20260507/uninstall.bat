@echo off
echo 🚣 Skelskør Roklub Timer - Afinstallation

echo.
echo Dette vil fjerne Skelskør Roklub Timer fra din computer.
echo ADVARSEL: Alle gemte konkurrence data vil blive slettet!
echo.

set /p confirm="Er du sikker på du vil afinstallere? (j/N): "
if /i not "%confirm%"=="j" (
    echo Afinstallation afbrudt.
    pause
    exit /b 0
)

echo.
echo 🧹 Fjerner filer...

REM Remove desktop shortcut if it exists
del "%USERPROFILE%\Desktop\Skelskør Roklub Timer.lnk" 2>nul

REM Remove application data
del "rowing_data.json" 2>nul
del "rowing_results_*.csv" 2>nul
del "rowing_results_*.pdf" 2>nul

echo ✅ Skelskør Roklub Timer er afinstalleret
echo 💾 Du kan nu slette denne mappe manuelt
echo.
echo 👋 Tak for at bruge Skelskør Roklub Timer!
echo    Velkommen tilbage på vandet snart! 🚣

pause

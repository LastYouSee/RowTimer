@echo off
echo 🚣 Opretter genvej til Skelskør Roklub Timer...

set "source=%~dp0SkelskørRoklub_Timer.exe"
set "desktop=%USERPROFILE%\Desktop"
set "shortcut=%desktop%\Skelskør Roklub Timer.lnk"

if exist "%source%" (
    powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut%'); $Shortcut.TargetPath = '%source%'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Skelskør Roklub Ro Konkurrence Timer'; $Shortcut.Save()"

    if exist "%shortcut%" (
        echo ✅ Genvej oprettet på skrivebordet!
        echo 📍 Placering: %shortcut%
        echo 🎯 Du kan nu starte programmet fra skrivebordet
    ) else (
        echo ❌ Kunne ikke oprette genvej
        echo 💡 Prøv at køre som administrator
    )
) else (
    echo ❌ Kan ikke finde SkelskørRoklub_Timer.exe
    echo 💡 Sørg for at alle filer er kopieret korrekt
)

echo.
pause

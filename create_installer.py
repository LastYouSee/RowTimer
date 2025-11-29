#!/usr/bin/env python3
"""
Skelskør Roklub - Simple Installer Creator
This script creates a simple installer for the rowing timer application.
"""

import os
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path


def create_installer_package():
    """Create a complete installer package for Skelskør Roklub"""
    print("🚣 Creating Skelskør Roklub Timer Installer Package...")
    print("=" * 60)

    # Check if executable exists
    exe_path = "SkelskørRoklub_Timer_Distribution/SkelskørRoklub_Timer.exe"
    if not os.path.exists(exe_path):
        print("❌ Executable not found!")
        print(f"   Looking for: {exe_path}")
        print("   Please build the executable first using:")
        print("   python build_executable.py")
        return False

    # Create installer directory
    installer_name = (
        f"SkelskørRoklub_Timer_Installer_{datetime.now().strftime('%Y%m%d')}"
    )
    installer_dir = Path(installer_name)

    if installer_dir.exists():
        print(f"🧹 Removing existing installer directory...")
        shutil.rmtree(installer_dir)

    installer_dir.mkdir()
    print(f"📁 Created installer directory: {installer_dir}")

    # Copy executable and files
    print("📋 Copying application files...")

    source_dir = Path("SkelskørRoklub_Timer_Distribution")
    files_to_copy = [
        "SkelskørRoklub_Timer.exe",
        "README.md",
        "USER_GUIDE.md",
        "IMPROVEMENTS.md",
        "club_logo.txt",
        "LÆSMIG_FØRST.txt",
    ]

    for file_name in files_to_copy:
        source = source_dir / file_name
        if source.exists():
            shutil.copy2(source, installer_dir / file_name)
            print(f"   ✅ {file_name}")
        else:
            print(f"   ⚠️ {file_name} (not found)")

    # Create installation guide
    create_installation_guide(installer_dir)

    # Create desktop shortcut script
    create_shortcut_script(installer_dir)

    # Create uninstaller
    create_uninstaller(installer_dir)

    # Create ZIP package
    create_zip_package(installer_dir, installer_name)

    print("\n" + "=" * 60)
    print("🎉 INSTALLER PACKAGE CREATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"📦 Installer folder: {installer_dir}")
    print(f"📦 ZIP package: {installer_name}.zip")

    # Show contents
    print(f"\n📋 Package contents:")
    for item in sorted(installer_dir.iterdir()):
        if item.is_file():
            size_kb = item.stat().st_size // 1024
            print(f"   📄 {item.name} ({size_kb} KB)")

    print(f"\n🚀 Ready for distribution to Skelskør Roklub members!")
    return True


def create_installation_guide(installer_dir):
    """Create comprehensive installation guide"""
    guide_content = """
🚣 SKELSKØR ROKLUB - RO KONKURRENCE TIMER 🚣
INSTALLATIONS GUIDE

═══════════════════════════════════════════════════════════════
📋 HVAD ER DETTE?
═══════════════════════════════════════════════════════════════

Dette er Skelskør Roklub's officielle Ro Konkurrence Timer - et
professionelt system til tidtagning ved ro-arrangementer.

Applikationen er udviklet specielt til Skelskør Roklub med:
✅ Dansk interface og branding
✅ Professionel tidtagning af ro-konkurrencer
✅ CSV og PDF eksport af resultater
✅ Individuelle båd kontroller
✅ Automatisk data gem-funktion

═══════════════════════════════════════════════════════════════
🚀 INSTALLATION (MEGET SIMPEL!)
═══════════════════════════════════════════════════════════════

TRIN 1: Opret mappe
   • Opret en mappe på dit skrivebord kaldet "SkelskørRoklub_Timer"
   • Eller vælg en anden placering hvor du vil have programmet

TRIN 2: Kopier filer
   • Kopier ALLE filer fra denne installationspakke til mappen
   • Vigtige filer:
     - SkelskørRoklub_Timer.exe (hovedprogrammet)
     - README.md (dokumentation)
     - USER_GUIDE.md (bruger guide)
     - club_logo.txt (klub information)

TRIN 3: Opret genvej (valgfrit)
   • Højreklik på "SkelskørRoklub_Timer.exe"
   • Vælg "Send til" → "Skrivebord (opret genvej)"
   • Eller kør "create_shortcut.bat" filen

TRIN 4: Test installation
   • Dobbeltklik på "SkelskørRoklub_Timer.exe"
   • Programmet skulle starte med Skelskør Roklub branding
   • Hvis det virker - installation er færdig! 🎉

═══════════════════════════════════════════════════════════════
💡 FØRSTE GANG DU BRUGER PROGRAMMET
═══════════════════════════════════════════════════════════════

1. Start programmet ved at dobbeltklikke på exe-filen
2. Gå til "Tilmeldinger" fanen for at registrere deltagere
3. Skift til "Tidtagning" fanen for at tage tid
4. Brug "Resultater" fanen til at se placeringer og eksportere
5. Læs "USER_GUIDE.md" for detaljerede instruktioner

═══════════════════════════════════════════════════════════════
🔧 SYSTEMKRAV
═══════════════════════════════════════════════════════════════

✅ Windows 10 eller nyere
✅ Ca. 50 MB ledig plads på harddisken
✅ Ingen yderligere programmer påkrævet
✅ Fungerer uden internet forbindelse

═══════════════════════════════════════════════════════════════
❓ PROBLEMER ELLER SPØRGSMÅL?
═══════════════════════════════════════════════════════════════

Hvis programmet ikke starter:
1. Prøv at højreklikke og "Kør som administrator"
2. Tjek at Windows Defender ikke blokerer filen
3. Sørg for at alle filer er kopieret korrekt

Kontakt Skelskør Roklub:
📍 Gammelgade 25, 4230 Skælskør
📞 +45 40 73 16 60
📧 skelskoerroklub@gmail.com
🌐 www.skelskoerroklub.dk

═══════════════════════════════════════════════════════════════
🚣 GOD KONKURRENCE! 🚣
═══════════════════════════════════════════════════════════════

© 2024 Skelskør Roklub
"Sammen på vandet - sammen i fællesskabet"
"""

    with open(installer_dir / "INSTALLATION_GUIDE.txt", "w", encoding="utf-8") as f:
        f.write(guide_content)

    print("   ✅ INSTALLATION_GUIDE.txt")


def create_shortcut_script(installer_dir):
    """Create batch script for creating desktop shortcut"""
    shortcut_script = """@echo off
echo 🚣 Opretter genvej til Skelskør Roklub Timer...

set "source=%~dp0SkelskørRoklub_Timer.exe"
set "desktop=%USERPROFILE%\\Desktop"
set "shortcut=%desktop%\\Skelskør Roklub Timer.lnk"

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
"""

    with open(installer_dir / "create_shortcut.bat", "w", encoding="utf-8") as f:
        f.write(shortcut_script)

    print("   ✅ create_shortcut.bat")


def create_uninstaller(installer_dir):
    """Create simple uninstaller script"""
    uninstaller_script = """@echo off
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
del "%USERPROFILE%\\Desktop\\Skelskør Roklub Timer.lnk" 2>nul

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
"""

    with open(installer_dir / "uninstall.bat", "w", encoding="utf-8") as f:
        f.write(uninstaller_script)

    print("   ✅ uninstall.bat")


def create_zip_package(installer_dir, installer_name):
    """Create ZIP package for easy distribution"""
    zip_path = f"{installer_name}.zip"

    print(f"📦 Creating ZIP package: {zip_path}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in installer_dir.rglob("*"):
            if file_path.is_file():
                arc_path = file_path.relative_to(installer_dir)
                zip_file.write(file_path, arc_path)
                print(f"   📄 Added {arc_path}")

    zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"   ✅ ZIP package created ({zip_size_mb:.1f} MB)")


def main():
    """Main installer creation function"""
    print("🏗️ Skelskør Roklub Timer - Installer Creator")
    print()

    # Check current directory
    if not os.path.exists("rowing_timer.py"):
        print("❌ Please run this script from the RowTimer directory")
        print("   Current directory should contain rowing_timer.py")
        input("\nPress Enter to exit...")
        return False

    try:
        success = create_installer_package()

        if success:
            print("\n🎉 Installer package ready for distribution!")
            print("📧 Send the ZIP file to Skelskør Roklub members")
            print("📋 They can extract and follow INSTALLATION_GUIDE.txt")
        else:
            print("\n❌ Failed to create installer package")

        return success

    except Exception as e:
        print(f"\n💥 Error creating installer: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        success = main()
        input(f"\n{'✅ Complete!' if success else '❌ Failed'} Press Enter to exit...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Installer creation cancelled")
        sys.exit(1)

#!/usr/bin/env python3
"""
Skelskør Roklub - Build Script for Executable
This script builds the rowing timer application into a standalone executable using PyInstaller.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking build dependencies...")

    # Check PyInstaller
    try:
        import PyInstaller

        print(f"✅ PyInstaller {PyInstaller.__version__} available")
    except ImportError:
        print("❌ PyInstaller not found")
        print("   Install with: pip install pyinstaller")
        return False

    # Check ReportLab
    try:
        import reportlab

        print("✅ ReportLab available for PDF export")
    except ImportError:
        print("⚠️ ReportLab not found - PDF export will not work in executable")
        print("   Install with: pip install reportlab")

    # Check main application
    if not os.path.exists("rowing_timer.py"):
        print("❌ rowing_timer.py not found in current directory")
        return False

    print("✅ Main application file found")
    return True


def create_icon():
    """Create a simple icon file for the executable"""
    print("🎨 Creating application icon...")

    # Try to create a simple ICO file programmatically
    try:
        from PIL import Image, ImageDraw, ImageFont

        # Create a 64x64 icon with rowing theme
        size = (64, 64)
        img = Image.new("RGBA", size, (30, 58, 138, 255))  # Club blue background
        draw = ImageDraw.Draw(img)

        # Draw a simple boat shape
        draw.ellipse([10, 25, 54, 35], fill="white")
        draw.rectangle([15, 28, 49, 32], fill=(30, 58, 138, 255))

        # Save as ICO
        img.save("club_icon.ico", format="ICO")
        print("✅ Created club_icon.ico")
        return True

    except ImportError:
        print("⚠️ PIL not available - creating text-based icon placeholder")

    # Create a simple placeholder icon using available tools
    icon_content = """
    🚣 Skelskør Roklub Timer Icon Placeholder
    This file serves as a reference for the executable icon.
    For best results, replace with a proper .ico file.
    """

    with open("club_icon.txt", "w", encoding="utf-8") as f:
        f.write(icon_content)

    print("📝 Created icon placeholder")
    return False


def clean_build_directories():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous build artifacts...")

    directories_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec~"]

    for dir_name in directories_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")

    print("✅ Build directories cleaned")


def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building Skelskør Roklub Timer executable...")

    # PyInstaller command with all necessary options
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--name",
        "SkelskørRoklub_Timer",
        "--distpath",
        "dist",
        "--workpath",
        "build",
        "--specpath",
        ".",
        # Include data files
        "--add-data",
        "club_logo.txt;.",
        "--add-data",
        "README.md;.",
        "--add-data",
        "USER_GUIDE.md;.",
        "--add-data",
        "IMPROVEMENTS.md;.",
        "--add-data",
        "requirements.txt;.",
        # Hidden imports for tkinter and reportlab
        "--hidden-import",
        "tkinter",
        "--hidden-import",
        "tkinter.ttk",
        "--hidden-import",
        "tkinter.filedialog",
        "--hidden-import",
        "tkinter.messagebox",
        "--hidden-import",
        "reportlab.platypus",
        "--hidden-import",
        "reportlab.lib.pagesizes",
        "--hidden-import",
        "reportlab.lib.styles",
        "--hidden-import",
        "reportlab.lib.colors",
        "--hidden-import",
        "reportlab.lib.enums",
        "--hidden-import",
        "reportlab.lib.units",
        # Exclude unnecessary modules to reduce size
        "--exclude-module",
        "matplotlib",
        "--exclude-module",
        "numpy",
        "--exclude-module",
        "pandas",
        "--exclude-module",
        "openpyxl",
        "--exclude-module",
        "PIL",
        # Version info
        "--version-file",
        "version_info.txt",
        # Main script
        "rowing_timer.py",
    ]

    # Add icon if available
    if os.path.exists("club_icon.ico"):
        cmd.extend(["--icon", "club_icon.ico"])
        print("   Using club_icon.ico for executable icon")

    try:
        print("   Running PyInstaller...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error code {e.returncode}")
        print("   STDOUT:", e.stdout)
        print("   STDERR:", e.stderr)
        return False


def create_version_info():
    """Create version info file for Windows executable"""
    print("📋 Creating version information...")

    version_info = """
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Skelskør Roklub'),
        StringStruct(u'FileDescription', u'Skelskør Roklub Ro Konkurrence Timer'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'SkelskørRoklub_Timer'),
        StringStruct(u'LegalCopyright', u'© 2024 Skelskør Roklub'),
        StringStruct(u'OriginalFilename', u'SkelskørRoklub_Timer.exe'),
        StringStruct(u'ProductName', u'Skelskør Roklub Timer'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""

    with open("version_info.txt", "w", encoding="utf-8") as f:
        f.write(version_info)

    print("✅ Version info created")


def create_distribution_package():
    """Create a distribution package with executable and documentation"""
    if not os.path.exists("dist/SkelskørRoklub_Timer.exe"):
        print("❌ Executable not found in dist directory")
        return False

    print("📦 Creating distribution package...")

    # Create distribution directory
    dist_dir = "SkelskørRoklub_Timer_Distribution"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    os.makedirs(dist_dir)

    # Copy executable
    shutil.copy("dist/SkelskørRoklub_Timer.exe", dist_dir)
    print("   Copied executable")

    # Copy documentation
    docs_to_copy = ["README.md", "USER_GUIDE.md", "IMPROVEMENTS.md", "club_logo.txt"]

    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy(doc, dist_dir)
            print(f"   Copied {doc}")

    # Create usage instructions
    usage_instructions = """
🚣 SKELSKØR ROKLUB - RO KONKURRENCE TIMER 🚣

INSTALLATION OG BRUG:
═══════════════════════════════════════════════════════════════

📁 FILER I DENNE PAKKE:
• SkelskørRoklub_Timer.exe - Hoved applikationen
• README.md - Generel information og funktioner
• USER_GUIDE.md - Detaljeret bruger guide
• IMPROVEMENTS.md - Tekniske forbedringer og funktioner
• club_logo.txt - Klubbens logo og information

🚀 SÅDAN STARTER DU PROGRAMMET:
1. Dobbeltklik på "SkelskørRoklub_Timer.exe"
2. Programmet starter med Skelskør Roklub branding
3. Ingen installation nødvendig - kører direkte

📋 SYSTEMKRAV:
• Windows 10 eller nyere
• Ingen yderligere software krævet
• Cirka 50 MB ledig plads

🎯 FUNKTIONER:
✅ Dansk interface tilpasset Skelskør Roklub
✅ Individuelle båd kontroller for hurtig tidtagning
✅ Samtidige timer for flere både
✅ CSV og PDF eksport af resultater
✅ Automatisk gem og hent af data
✅ Professionel rangering baseret på konsistens

📞 SUPPORT:
Skelskør Roklub
Gammelgade 25, 4230 Skælskør
Tel: +45 40 73 16 60
Web: www.skelskoerroklub.dk

═══════════════════════════════════════════════════════════════
© 2024 Skelskør Roklub - Sammen på vandet, sammen i fællesskabet
═══════════════════════════════════════════════════════════════
"""

    with open(f"{dist_dir}/LÆSMIG_FØRST.txt", "w", encoding="utf-8") as f:
        f.write(usage_instructions)

    print(f"✅ Distribution package created: {dist_dir}/")
    return True


def main():
    """Main build function"""
    print("=" * 60)
    print("🚣 SKELSKØR ROKLUB - EXECUTABLE BUILD SCRIPT 🚣")
    print("=" * 60)
    print("Building standalone executable for Ro Konkurrence Timer")
    print()

    # Check current directory
    if not os.path.exists("rowing_timer.py"):
        print("❌ Please run this script from the RowTimer directory")
        print("   Current directory should contain rowing_timer.py")
        return False

    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Build requirements not met")
        print("Install missing dependencies and try again")
        return False

    print()

    # Step 2: Create version info and icon
    create_version_info()
    create_icon()

    print()

    # Step 3: Clean previous builds
    clean_build_directories()

    print()

    # Step 4: Build executable
    if not build_executable():
        print("\n❌ Build failed")
        return False

    print()

    # Step 5: Create distribution package
    if not create_distribution_package():
        print("\n⚠️ Distribution package creation failed")
        print("But executable should be available in dist/ directory")

    print()
    print("=" * 60)
    print("🎉 BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 60)

    # Show build results
    exe_path = "dist/SkelskørRoklub_Timer.exe"
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"📁 Executable: {exe_path}")
        print(f"💾 Size: {size_mb:.1f} MB")
        print(f"🎯 Distribution: SkelskørRoklub_Timer_Distribution/")
        print()
        print("✅ Ready for distribution to Skelskør Roklub!")
        print("🚣 The executable includes full Danish branding and functionality")

    return True


if __name__ == "__main__":
    try:
        success = main()

        if success:
            input("\n🎉 Build successful! Press Enter to exit...")
        else:
            input("\n❌ Build failed. Press Enter to exit...")

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n⏹️ Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)

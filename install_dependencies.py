#!/usr/bin/env python3
"""
Rowing Timer - Dependency Installation Script
This script installs the required dependencies for the rowing timer application.
"""

import os
import subprocess
import sys


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("❌ Python 3.6 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False

    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "--version"], check=True, capture_output=True
        )
        print("✅ pip is available")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        return False


def install_package(package_name, description=""):
    """Install a single package"""
    try:
        print(f"📦 Installing {package_name}...")
        if description:
            print(f"   Purpose: {description}")

        subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name], check=True
        )
        print(f"✅ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        return False


def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter

        print("✅ tkinter is available")
        return True
    except ImportError:
        print("❌ tkinter is not available")
        print("   Note: tkinter is usually included with Python installations")
        print("   On Linux, you may need to install python3-tk package")
        return False


def main():
    """Main installation function"""
    print("=" * 60)
    print("🚣‍♀️ ROWING TIMER - DEPENDENCY INSTALLER")
    print("=" * 60)
    print()

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Check pip
    if not check_pip():
        print("\nPlease install pip first:")
        print("https://pip.pypa.io/en/stable/installation/")
        sys.exit(1)

    # Check tkinter
    if not check_tkinter():
        if sys.platform.startswith("linux"):
            print("\nOn Ubuntu/Debian, install with:")
            print("sudo apt-get install python3-tk")
        elif sys.platform == "darwin":
            print("\nOn macOS with Homebrew:")
            print("brew install python-tk")
        sys.exit(1)

    print()
    print("📋 Installing dependencies...")
    print()

    # Define packages to install
    packages = [
        ("reportlab>=3.5.0", "PDF export functionality"),
    ]

    # Optional packages that enhance functionality
    optional_packages = [
        ("matplotlib>=3.5.0", "Time graphs and visualizations"),
        ("pandas>=1.3.0", "Advanced data analysis"),
        ("openpyxl>=3.0.0", "Excel export functionality"),
    ]

    # Install required packages
    all_success = True
    for package, description in packages:
        if not install_package(package, description):
            all_success = False

    # Ask about optional packages
    print()
    if (
        input("📦 Would you like to install optional packages? (y/N): ")
        .lower()
        .startswith("y")
    ):
        print("\n📦 Installing optional packages...")
        for package, description in optional_packages:
            install_package(package, description)

    print()
    print("=" * 60)

    if all_success:
        print("🎉 INSTALLATION COMPLETE!")
        print()
        print("✅ All required dependencies installed successfully")
        print("🚀 You can now run the rowing timer:")
        print("   python rowing_timer.py")
        print()
        print("📋 Features available:")
        print("   • Participant registration")
        print("   • Individual boat timing controls")
        print("   • Real-time timer displays")
        print("   • Consistency-based rankings")
        print("   • CSV export")
        print("   • PDF export (with reportlab)")
        print("   • Data persistence")
    else:
        print("⚠️ INSTALLATION COMPLETED WITH WARNINGS")
        print()
        print("Some packages failed to install, but basic functionality should work.")
        print("PDF export may not be available without reportlab.")
        print()
        print("You can still run: python rowing_timer.py")

    print()
    print("📚 For help and documentation, see:")
    print("   • README.md - Overview and quick start")
    print("   • USER_GUIDE.md - Detailed usage instructions")
    print("   • IMPROVEMENTS.md - Feature improvements")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

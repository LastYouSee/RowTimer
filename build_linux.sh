#!/bin/bash
set -e

# Skelskør Roklub - Linux Build Script
# Works on Native Linux (Mint/Ubuntu) and WSL

echo "🚣 SKELSKØR ROKLUB - LINUX BUILD SCRIPT"
echo "========================================="

# Function to check and install dependencies
check_dependencies() {
    echo "🔍 Checking system dependencies..."
    
    # List of required packages
    PACKAGES="python3 python3-pip python3-venv python3-tk binutils"
    MISSING_PACKAGES=""

    for pkg in $PACKAGES; do
        if ! dpkg -s $pkg >/dev/null 2>&1; then
            MISSING_PACKAGES="$MISSING_PACKAGES $pkg"
        fi
    done

    if [ -n "$MISSING_PACKAGES" ]; then
        echo "⚠️ Missing packages:$MISSING_PACKAGES"
        if [ "$EUID" -ne 0 ]; then
            echo "🔧 Asking for sudo permission to install dependencies..."
            sudo apt-get update
            sudo apt-get install -y $MISSING_PACKAGES
        else
            apt-get update
            apt-get install -y $MISSING_PACKAGES
        fi
    else
        echo "✅ System dependencies met."
    fi
}

# Run dependency check
check_dependencies

# Setup Python environment
echo "🐍 Setting up Python virtual environment..."
if [ -d "linux_build_env" ]; then
    echo "   Using existing venv..."
else
    python3 -m venv linux_build_env
    echo "   Created new venv."
fi

source linux_build_env/bin/activate

# Install Python requirements
echo "📦 Installing Python requirements..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found, installing reportlab manually..."
    pip install reportlab
fi
pip install pyinstaller

# Clean previous builds
echo "🧹 Cleaning up..."
rm -rf build dist
rm -f *.spec

# Build with PyInstaller
echo "🔨 Building with PyInstaller..."
# Note: Linux uses ':' separator for --add-data, Windows uses ';'
pyinstaller --noconfirm --onefile --windowed \
    --name "SkelskørRoklub_Timer_Linux" \
    --add-data "club_logo.png:." \
    --add-data "club_logo.txt:." \
    --add-data "README.md:." \
    --add-data "USER_GUIDE.md:." \
    --add-data "IMPROVEMENTS.md:." \
    --hidden-import "tkinter" \
    --hidden-import "reportlab" \
    rowing_timer.py

# Deactivate venv
deactivate

# Organize output
echo "📦 Packaging..."
DIST_DIR="dist_linux"
rm -rf $DIST_DIR
mkdir -p $DIST_DIR

if [ -f "dist/SkelskørRoklub_Timer_Linux" ]; then
    mv dist/SkelskørRoklub_Timer_Linux $DIST_DIR/
    echo "✅ Executable moved to $DIST_DIR/"
else
    echo "❌ Build failed - Executable not found!"
    exit 1
fi

# Copy documentation to dist folder
cp README.md USER_GUIDE.md IMPROVEMENTS.md club_logo.txt club_logo.png $DIST_DIR/ 2>/dev/null || true

echo "========================================="
echo "🎉 Linux Build Complete!"
echo "📁 Output directory: $DIST_DIR"
echo "🏃 Run with: ./$DIST_DIR/SkelskørRoklub_Timer_Linux"

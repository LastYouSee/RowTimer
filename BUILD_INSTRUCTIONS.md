# Skelskør Roklub - Build Instructions for Executable

## 🚣 Building the Standalone Executable

This guide explains how to create a standalone executable (.exe) file for the Skelskør Roklub Rowing Timer application using PyInstaller.

## 📋 Prerequisites

### Required Software
- **Python 3.6 or higher** installed on Windows
- **pip** package manager (included with Python)

### Required Python Packages
```bash
pip install pyinstaller
pip install reportlab
```

Or install all dependencies at once:
```bash
pip install -r requirements.txt
```

## 🔨 Build Methods

### Method 1: Automated Build Script (Recommended)

The easiest way to build the executable:

```bash
python build_executable.py
```

This script will:
- ✅ Check all dependencies
- ✅ Create application icon
- ✅ Clean previous builds
- ✅ Build the executable
- ✅ Create distribution package
- ✅ Include all documentation

**Output**: Complete distribution package in `SkelskørRoklub_Timer_Distribution/`

### Method 2: Windows Batch File

For Windows users who prefer double-clicking:

```bash
build_exe.bat
```

Double-click the file and it will automatically build the executable.

### Method 3: Manual PyInstaller Command

For advanced users or custom builds:

```bash
python -m PyInstaller --onefile --windowed --name "SkelskørRoklub_Timer" --add-data "club_logo.txt;." --add-data "README.md;." --add-data "USER_GUIDE.md;." --hidden-import "tkinter" --hidden-import "tkinter.ttk" --hidden-import "tkinter.filedialog" --hidden-import "tkinter.messagebox" --hidden-import "reportlab.platypus" --hidden-import "reportlab.lib.pagesizes" --hidden-import "reportlab.lib.styles" --hidden-import "reportlab.lib.colors" --exclude-module "matplotlib" --exclude-module "numpy" --exclude-module "pandas" rowing_timer.py
```

## 📁 Build Output

### File Structure After Build
```
RowTimer/
├── dist/                           # PyInstaller output directory
│   └── SkelskørRoklub_Timer.exe   # Main executable
├── build/                          # Build artifacts (can be deleted)
├── SkelskørRoklub_Timer_Distribution/  # Ready-to-distribute package
│   ├── SkelskørRoklub_Timer.exe   # Main executable
│   ├── README.md                   # Application documentation
│   ├── USER_GUIDE.md              # User guide
│   ├── IMPROVEMENTS.md            # Technical improvements
│   ├── club_logo.txt              # Club branding
│   └── LÆSMIG_FØRST.txt          # Danish usage instructions
└── SkelskørRoklub_Timer.spec      # PyInstaller configuration
```

### Executable Details
- **Name**: `SkelskørRoklub_Timer.exe`
- **Size**: ~15-20 MB
- **Type**: Windows executable (no console)
- **Dependencies**: Self-contained (no external files needed)
- **Icon**: Custom Skelskør Roklub icon

## 🎯 Distribution Package Contents

The `SkelskørRoklub_Timer_Distribution` folder contains everything needed for distribution:

### Files Included
1. **SkelskørRoklub_Timer.exe** - The main application
2. **LÆSMIG_FØRST.txt** - Danish installation and usage instructions
3. **README.md** - English documentation and features
4. **USER_GUIDE.md** - Detailed user guide
5. **IMPROVEMENTS.md** - Technical improvements and features
6. **club_logo.txt** - Club branding information

### Ready for Distribution
- ✅ No installation required
- ✅ Self-contained executable
- ✅ Includes all documentation
- ✅ Professional Danish branding
- ✅ Suitable for club distribution

## 🔧 Build Configuration

### PyInstaller Settings Used
- `--onefile`: Creates single executable file
- `--windowed`: No console window (GUI only)
- `--name`: Custom executable name
- `--add-data`: Includes documentation files
- `--hidden-import`: Ensures tkinter and reportlab are included
- `--exclude-module`: Removes unnecessary large packages

### Included Data Files
- `club_logo.txt` - Club branding and logo
- `README.md` - Main documentation
- `USER_GUIDE.md` - User instructions
- `IMPROVEMENTS.md` - Technical details

### Hidden Imports (Automatically Included)
- `tkinter` - GUI framework
- `tkinter.ttk` - Enhanced GUI widgets
- `tkinter.filedialog` - File selection dialogs
- `tkinter.messagebox` - Message dialogs
- `reportlab.*` - PDF generation libraries

### Excluded Modules (Reduces Size)
- `matplotlib` - Plotting library (not used)
- `numpy` - Scientific computing (not used)
- `pandas` - Data analysis (not used)
- `openpyxl` - Excel support (not used)

## 🚀 Testing the Executable

### Basic Test
1. Navigate to `dist/` or `SkelskørRoklub_Timer_Distribution/`
2. Double-click `SkelskørRoklub_Timer.exe`
3. Application should start with Skelskør Roklub branding
4. Test basic functionality (registration, timing, export)

### Function Tests
- ✅ Participant registration
- ✅ Timer start/stop functionality
- ✅ CSV export (should work)
- ✅ PDF export (should work if ReportLab was included)
- ✅ Data persistence (creates .json file in same directory)

## 📦 Distribution Instructions

### For Club Members
1. Copy the entire `SkelskørRoklub_Timer_Distribution` folder to target computer
2. Double-click `SkelskørRoklub_Timer.exe` to run
3. First read `LÆSMIG_FØRST.txt` for Danish instructions

### For Official Events
- The executable is ready for professional use
- Includes full Skelskør Roklub branding
- Danish interface suitable for local events
- Professional PDF exports for official documentation

## 🐛 Troubleshooting

### Common Build Issues

**"PyInstaller not found"**
```bash
pip install pyinstaller
```

**"ReportLab not found"**
```bash
pip install reportlab
```

**Build fails with permission errors**
- Run command prompt as Administrator
- Ensure antivirus is not blocking PyInstaller

**Executable won't start**
- Check Windows Defender/antivirus settings
- Try running from different location
- Check that all source files are present during build

### Runtime Issues

**PDF export doesn't work**
- ReportLab wasn't included in build
- Rebuild with ReportLab installed

**Application crashes on startup**
- Missing data files (club_logo.txt, etc.)
- Rebuild with `--add-data` parameters

**Danish characters not displaying correctly**
- Use UTF-8 encoding in source files
- Ensure Windows supports Unicode display

## 🔄 Updating the Executable

When application code changes:

1. Update the source files
2. Test the application normally (`python rowing_timer.py`)
3. Rebuild the executable using preferred method
4. Test the new executable
5. Replace old version in distribution

## 📊 Build Performance

### Typical Build Times
- **Simple build**: 30-60 seconds
- **Full build with all data**: 60-120 seconds
- **Clean build (first time)**: 120-180 seconds

### File Sizes
- **Source code**: ~100 KB
- **Executable**: ~15-20 MB
- **Distribution package**: ~20-25 MB

## 🎉 Success Indicators

Build is successful when you see:
```
INFO: Building EXE from EXE-00.toc completed successfully.
✅ Ready for distribution to Skelskør Roklub!
🚣 The executable includes full Danish branding and functionality
```

The executable should:
- Start without console window
- Display Skelskør Roklub branding
- Function identically to Python version
- Export CSV and PDF files correctly
- Save data persistently

---

## 💡 Tips for Best Results

1. **Always test** the executable before distributing
2. **Include all documentation** files in distribution
3. **Use meaningful version numbers** for tracking
4. **Test on clean Windows machine** without Python installed
5. **Keep source code backup** for future updates

---

*Built with ❤️ for Skelskør Roklub*
*Sammen på vandet - sammen i fællesskabet* 🚣‍♀️🚣‍♂️
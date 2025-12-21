# Building for Linux

This guide covers how to build the Skelskør Roklub Rowing Timer for Linux.

## Requirements
- **Source Code**: The full python project.
- **System**: 
    - Native Linux (e.g., Linux Mint, Ubuntu, Debian)
    - OR Windows with WSL (Windows Subsystem for Linux) installed.

## Method 1: Native Linux (e.g., Linux Mint)

1. Open a terminal in the project directory.
2. Make the build script executable (first time only):
   ```bash
   chmod +x build_linux.sh
   ```
3. Run the build script:
   ```bash
   ./build_linux.sh
   ```
4. The script will:
   - Install system dependencies (`python3-tk`, `binutils`, etc.) via `apt-get` (may ask for sudo).
   - Create a virtual environment (`linux_build_env`).
   - Install Python dependencies (`requirements.txt`).
   - Build the executable using PyInstaller.
5. **Output**: The built application will be in the `dist_linux/` folder.

## Method 2: From Windows via WSL

1. Ensure you have WSL installed and a distribution (like Ubuntu) set up.
2. Open Command Prompt or PowerShell in the project directory.
3. Run the helper script:
   ```bash
   python build_linux_wsl.py
   ```
   *Note: This will automatically invoke `build_linux.sh` inside your WSL instance.*

## Output

The build process creates a standalone binary:
`dist_linux/SkelskørRoklub_Timer_Linux`

To run it:
```bash
./dist_linux/SkelskørRoklub_Timer_Linux
```

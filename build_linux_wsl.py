import subprocess
import sys
import shutil

def main():
    print("🚀 Starting Linux Build via WSL...")
    
    import platform
    
    # Check if running on Linux (Native or WSL)
    if platform.system() == "Linux":
        print("🐧 Running on Linux...")
        cmd = ["bash", "build_linux.sh"]
    else:
        # We are on Windows, try to use WSL
        if not shutil.which("wsl"):
            print("❌ WSL (Windows Subsystem for Linux) is not found in PATH.")
            print("   Please install WSL to build for Linux from Windows.")
            sys.exit(1)

        # Command to run the shell script inside WSL
        # Converts CRLF to LF just in case, then runs it
        cmd = ["wsl", "bash", "-c", "dos2unix build_linux.sh 2>/dev/null || true; bash build_linux.sh"]
    
    try:
        print("   Executing build_linux.sh in WSL...")
        result = subprocess.run(cmd, check=True)
        if result.returncode == 0:
            print("\n✅ Build command finished successfully.")
            print("   Check the 'dist_linux' folder in your project directory.")
        else:
            print("\n❌ Build failed with error code:", result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Execution failed: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Build cancelled.")

if __name__ == "__main__":
    main()

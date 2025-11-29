#!/usr/bin/env python3
"""
Rowing Timer Application Launcher
Simple launcher script for the rowing event timer application.
"""

import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rowing_timer import main

    if __name__ == "__main__":
        print("Starting Rowing Timer Application...")
        main()

except ImportError as e:
    print(f"Error importing rowing_timer module: {e}")
    print("Please ensure rowing_timer.py is in the same directory.")
    sys.exit(1)

except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1)

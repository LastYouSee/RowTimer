#!/usr/bin/env python3
"""
Rowing Timer - Interactive Demo
This script demonstrates the new individual boat controls interface.
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rowing_timer import RowingTimer
except ImportError as e:
    print(f"Error importing rowing_timer module: {e}")
    print("Please ensure rowing_timer.py is in the same directory.")
    sys.exit(1)


def create_demo_data():
    """Create demo data to showcase the interface"""
    demo_data = {
        "B001": {
            "name": "Lightning Bolt",
            "run1_time": 67.234,
            "run2_time": None,
            "run1_start": None,
            "run2_start": None,
        },
        "B002": {
            "name": "Thunder Strike",
            "run1_time": None,
            "run2_time": None,
            "run1_start": None,
            "run2_start": None,
        },
        "B003": {
            "name": "Wave Rider",
            "run1_time": 65.890,
            "run2_time": 66.123,
            "run1_start": None,
            "run2_start": None,
        },
        "B004": {
            "name": "Storm Chaser",
            "run1_time": None,
            "run2_time": None,
            "run1_start": None,
            "run2_start": None,
        },
        "B005": {
            "name": "Ocean Master",
            "run1_time": 70.456,
            "run2_time": None,
            "run1_start": None,
            "run2_start": None,
        },
    }
    return demo_data


def show_demo_dialog():
    """Show demo introduction dialog"""
    root = tk.Tk()
    root.withdraw()

    message = (
        "🚣‍♀️ ROWING TIMER DEMO 🚣‍♂️\n\n"
        "This demo showcases the NEW Individual Boat Controls interface!\n\n"
        "✨ KEY IMPROVEMENTS:\n"
        "• Each boat has dedicated START/STOP/RESET buttons\n"
        "• No more dropdown selection needed\n"
        "• Perfect for timing multiple boats simultaneously\n"
        "• Visual status indicators for each boat\n"
        "• Faster operation during close race starts\n\n"
        "📋 DEMO DATA INCLUDES:\n"
        "• B001 Lightning Bolt (Run 1 complete)\n"
        "• B002 Thunder Strike (ready to time)\n"
        "• B003 Wave Rider (both runs complete)\n"
        "• B004 Storm Chaser (ready to time)\n"
        "• B005 Ocean Master (Run 1 complete)\n\n"
        "🎯 TRY THESE FEATURES:\n"
        "1. Go to Timing tab to see individual boat controls\n"
        "2. Switch between Run 1 and Run 2 modes\n"
        "3. Start/stop timers for different boats\n"
        "4. Check Results tab for rankings\n\n"
        "Ready to start the demo?"
    )

    result = messagebox.askyesno("Rowing Timer Demo", message)
    root.destroy()
    return result


def setup_demo_app(app):
    """Load demo data and setup the application"""
    try:
        # Load demo data
        demo_data = create_demo_data()
        app.participants.update(demo_data)
        app.save_data()

        # Update all displays
        app.update_participants_display()
        app.update_boat_controls()

        # Show helpful info
        messagebox.showinfo(
            "Demo Ready!",
            "🎉 Demo data loaded successfully!\n\n"
            "📍 NEXT STEPS:\n"
            "1. Check the Registration tab to see all boats\n"
            "2. Go to Timing tab to see the new interface\n"
            "3. Try timing boats B002 and B004\n"
            "4. Complete Run 2 for boats B001 and B005\n"
            "5. Calculate results to see rankings!\n\n"
            "💡 TIP: You can time multiple boats simultaneously\n"
            "by clicking different boats' START buttons!",
        )

        return True

    except Exception as e:
        messagebox.showerror("Demo Error", f"Failed to setup demo: {str(e)}")
        return False


def main():
    """Main demo function"""
    print("🚣‍♀️ Starting Rowing Timer Demo...")

    # Show introduction
    if not show_demo_dialog():
        print("Demo cancelled by user.")
        return

    try:
        # Create the application
        root = tk.Tk()
        app = RowingTimer(root)

        # Setup demo data
        if not setup_demo_app(app):
            return

        print("✅ Demo started successfully!")
        print("🎯 Try the new individual boat controls in the Timing tab!")
        print("📝 Close the application window when finished.")

        # Add demo title to window
        root.title("Rowing Timer - DEMO MODE (New Boat Controls)")

        # Start the GUI
        root.mainloop()

    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user.")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        messagebox.showerror("Demo Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()

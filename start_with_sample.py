#!/usr/bin/env python3
"""
Rowing Timer Application with Sample Data
This script starts the rowing timer application and optionally loads sample data for demonstration.
"""

import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rowing_timer import RowingTimer
except ImportError as e:
    print(f"Error importing rowing_timer module: {e}")
    print("Please ensure rowing_timer.py is in the same directory.")
    sys.exit(1)


def create_sample_data():
    """Create sample data for demonstration purposes"""
    sample_data = {
        "B001": {
            "name": "Alice Johnson",
            "run1_time": 65.234,
            "run2_time": 65.890,
            "run1_start": None,
            "run2_start": None,
        },
        "B002": {
            "name": "Bob Smith",
            "run1_time": 62.123,
            "run2_time": 63.456,
            "run1_start": None,
            "run2_start": None,
        },
        "B003": {
            "name": "Carol Davis",
            "run1_time": 68.567,
            "run2_time": 68.234,
            "run1_start": None,
            "run2_start": None,
        },
        "B004": {
            "name": "David Wilson",
            "run1_time": 61.789,
            "run2_time": 64.123,
            "run1_start": None,
            "run2_start": None,
        },
        "B005": {
            "name": "Emma Brown",
            "run1_time": 70.111,
            "run2_time": 70.222,
            "run1_start": None,
            "run2_start": None,
        },
        "B006": {
            "name": "Frank Miller",
            "run1_time": 59.876,
            "run2_time": None,
            "run1_start": None,
            "run2_start": None,
        },
        "B007": {
            "name": "Grace Taylor",
            "run1_time": None,
            "run2_time": None,
            "run1_start": None,
            "run2_start": None,
        },
    }
    return sample_data


def show_welcome_dialog():
    """Show welcome dialog with option to load sample data"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window temporarily

    # Check if data file exists
    data_file = "rowing_data.json"
    has_existing_data = os.path.exists(data_file) and os.path.getsize(data_file) > 0

    if has_existing_data:
        message = (
            "Welcome to the Rowing Event Timer!\n\n"
            "Existing data found. The application will load your previous session.\n\n"
            "Click OK to continue with existing data, or Cancel to exit."
        )

        result = messagebox.askokcancel("Rowing Timer - Existing Data", message)
        root.destroy()
        return result, False
    else:
        message = (
            "Welcome to the Rowing Event Timer!\n\n"
            "This appears to be your first time running the application.\n\n"
            "Would you like to load sample data for demonstration purposes?\n\n"
            "Sample data includes:\n"
            "• 7 registered participants\n"
            "• 5 with completed times (both runs)\n"
            "• 1 with partial data (one run only)\n"
            "• 1 with no times recorded\n\n"
            "Choose 'Yes' for sample data, 'No' for empty start, or 'Cancel' to exit."
        )

        result = messagebox.askyesnocancel("Rowing Timer - First Run", message)
        root.destroy()

        if result is None:  # Cancel
            return False, False
        elif result is True:  # Yes - load sample data
            return True, True
        else:  # No - start empty
            return True, False


def load_sample_data(app):
    """Load sample data into the application"""
    try:
        sample_data = create_sample_data()
        app.participants.update(sample_data)
        app.save_data()
        app.update_participants_display()
        app.update_boat_controls()

        # Show info about loaded data
        messagebox.showinfo(
            "Sample Data Loaded",
            "Sample data has been loaded!\n\n"
            "Check the Registration tab to see participants.\n"
            "Go to Results tab and click 'Calculate Results' to see rankings.\n\n"
            "You can now experiment with the timing features!",
        )
        return True

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load sample data: {str(e)}")
        return False


def main():
    """Main function to start the application"""
    print("Starting Rowing Timer Application...")

    # Show welcome dialog
    should_continue, load_sample = show_welcome_dialog()

    if not should_continue:
        print("Application cancelled by user.")
        return

    try:
        # Create the main application
        root = tk.Tk()
        app = RowingTimer(root)

        # Load sample data if requested
        if load_sample:
            print("Loading sample data...")
            load_sample_data(app)

        # Update displays initially
        app.update_participants_display()
        app.update_boat_controls()

        print("Application started successfully!")
        print("Close the application window to exit.")

        # Start the GUI event loop
        root.mainloop()

    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
    except Exception as e:
        print(f"Error running application: {e}")
        messagebox.showerror("Application Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()

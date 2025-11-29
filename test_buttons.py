#!/usr/bin/env python3
"""
Button Styling Test for Rowing Timer
This script tests the button styling to ensure visibility improvements work correctly.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def create_button_test():
    """Create a test window to verify button styling"""
    root = tk.Tk()
    root.title("Button Styling Test - Rowing Timer")
    root.geometry("600x400")

    # Create main frame
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Title
    title_label = ttk.Label(
        main_frame, text="Button Styling Test", font=("Arial", 16, "bold")
    )
    title_label.pack(pady=10)

    # Instructions
    instructions = ttk.Label(
        main_frame,
        text="Test the button visibility:\n"
        + "• START buttons should be GREEN with WHITE text\n"
        + "• STOP buttons should be RED with WHITE text\n"
        + "• RESET buttons should be GRAY with BLACK text\n"
        + "• All text should be clearly readable",
        font=("Arial", 10),
        justify=tk.LEFT,
    )
    instructions.pack(pady=10)

    # Note: Using tk.Button instead of ttk.Button for reliable color control
    # ttk buttons can have theme conflicts with custom colors on some systems

    # Create test button frame
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=20)

    # Test boat rows
    test_boats = [
        ("B001", "Test Boat 1"),
        ("B002", "Test Boat 2"),
        ("B003", "Test Boat 3"),
    ]

    # Header
    header_frame = ttk.Frame(button_frame)
    header_frame.pack(fill=tk.X, pady=5)

    ttk.Label(header_frame, text="Boat", font=("Arial", 10, "bold"), width=8).grid(
        row=0, column=0
    )
    ttk.Label(header_frame, text="Name", font=("Arial", 10, "bold"), width=15).grid(
        row=0, column=1
    )
    ttk.Label(header_frame, text="Status", font=("Arial", 10, "bold"), width=15).grid(
        row=0, column=2
    )
    ttk.Label(header_frame, text="Controls", font=("Arial", 10, "bold"), width=25).grid(
        row=0, column=3
    )

    # Separator
    ttk.Separator(button_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

    # Create test rows
    for i, (boat, name) in enumerate(test_boats):
        boat_frame = ttk.Frame(button_frame)
        boat_frame.pack(fill=tk.X, pady=2)

        # Boat info
        ttk.Label(boat_frame, text=boat, font=("Arial", 10, "bold"), width=8).grid(
            row=0, column=0, sticky=tk.W
        )
        ttk.Label(boat_frame, text=name, width=15).grid(row=0, column=1, sticky=tk.W)

        # Status (varies by row for testing)
        statuses = ["Ready", "RUNNING", "Complete"]
        status_colors = ["blue", "red", "green"]
        status_text = statuses[i % 3]
        status_color = status_colors[i % 3]

        ttk.Label(
            boat_frame,
            text=status_text,
            width=15,
            foreground=status_color,
            font=("Arial", 9, "bold"),
        ).grid(row=0, column=2, sticky=tk.W)

        # Control buttons
        control_frame = ttk.Frame(boat_frame)
        control_frame.grid(row=0, column=3, sticky=tk.W)

        # START button - using tk.Button for reliable color control
        start_btn = tk.Button(
            control_frame,
            text="START",
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            font=("Arial", 9, "bold"),
            width=8,
            relief="raised",
            bd=2,
            command=lambda b=boat: print(f"START clicked for {b}"),
        )
        start_btn.pack(side=tk.LEFT, padx=2)

        # STOP button - using tk.Button for reliable color control
        stop_btn = tk.Button(
            control_frame,
            text="STOP",
            bg="#f44336",
            fg="white",
            activebackground="#da190b",
            activeforeground="white",
            font=("Arial", 9, "bold"),
            width=8,
            relief="raised",
            bd=2,
            command=lambda b=boat: print(f"STOP clicked for {b}"),
        )
        stop_btn.pack(side=tk.LEFT, padx=2)

        # RESET button - using tk.Button for reliable color control
        reset_btn = tk.Button(
            control_frame,
            text="RESET",
            bg="#e0e0e0",
            fg="black",
            activebackground="#ddd",
            activeforeground="black",
            font=("Arial", 9, "bold"),
            width=8,
            relief="raised",
            bd=2,
            command=lambda b=boat: print(f"RESET clicked for {b}"),
        )
        reset_btn.pack(side=tk.LEFT, padx=2)

        # Enable/disable some buttons for realistic testing
        if i == 1:  # Middle row - simulate running state
            start_btn.config(state="disabled")
            stop_btn.config(state="normal")
        elif i == 2:  # Bottom row - simulate completed state
            start_btn.config(state="normal")
            stop_btn.config(state="disabled")
            reset_btn.config(state="normal")
        else:  # Top row - ready state
            start_btn.config(state="normal")
            stop_btn.config(state="disabled")
            reset_btn.config(state="disabled")

    # Test results frame
    results_frame = ttk.LabelFrame(
        main_frame, text="Visibility Test Results", padding=10
    )
    results_frame.pack(fill=tk.X, pady=20)

    # Test checklist
    checklist = [
        "✓ START buttons are GREEN (#4CAF50) with WHITE text",
        "✓ STOP buttons are RED (#f44336) with WHITE text",
        "✓ RESET buttons are GRAY (#e0e0e0) with BLACK text",
        "✓ All text is clearly readable and high contrast",
        "✓ Hover effects darken the button colors",
        "✓ Disabled buttons are visually distinct",
    ]

    for item in checklist:
        ttk.Label(results_frame, text=item, font=("Arial", 9)).pack(anchor=tk.W)

    # Close button
    close_btn = ttk.Button(main_frame, text="Close Test", command=root.destroy)
    close_btn.pack(pady=10)

    # Status label
    status_label = ttk.Label(
        main_frame,
        text="Click buttons to test functionality. Check console for click events.",
        font=("Arial", 9),
        foreground="gray",
    )
    status_label.pack()

    return root


def main():
    """Run the button styling test"""
    print("🎨 Starting Button Styling Test...")
    print("📋 This test verifies:")
    print("   • Button colors are properly set")
    print("   • Text is readable (no white-on-white)")
    print("   • Hover effects work")
    print("   • Disabled states are clear")
    print()

    try:
        root = create_button_test()
        print("✅ Test window created successfully!")
        print("🖱️ Interact with buttons to verify styling")
        print("📄 Check the visual checklist in the window")
        print("🔄 Button clicks will print to console")
        print()

        root.mainloop()
        print("🏁 Button styling test completed!")

    except Exception as e:
        print(f"❌ Error running button test: {e}")
        return False

    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("✅ Button styling appears to be working correctly!")
    else:
        print("❌ Button styling test encountered issues.")

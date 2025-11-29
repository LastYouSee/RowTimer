#!/usr/bin/env python3
"""
Button Color Demo for Rowing Timer
This demo specifically showcases the reliable button color solution using tk.Button.
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk


def create_button_demo():
    """Create a comprehensive demo of button styling solutions"""
    root = tk.Tk()
    root.title("Button Color Demo - Rowing Timer")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    # Main container
    main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Title
    title_label = tk.Label(
        main_frame,
        text="🎨 Button Color Solution Demo",
        font=("Arial", 18, "bold"),
        bg="#f0f0f0",
        fg="#333333",
    )
    title_label.pack(pady=(0, 10))

    # Problem description
    problem_frame = tk.LabelFrame(
        main_frame,
        text="❌ The Problem (Before)",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
        fg="#cc0000",
        padx=10,
        pady=10,
    )
    problem_frame.pack(fill=tk.X, pady=(0, 20))

    problem_text = tk.Label(
        problem_frame,
        text="• ttk.Button styling was unreliable across different systems\n"
        "• White text on white background made buttons unreadable\n"
        "• Theme conflicts caused styling to be overridden\n"
        "• Disabled states were not clearly visible",
        font=("Arial", 10),
        bg="#f0f0f0",
        justify=tk.LEFT,
    )
    problem_text.pack(anchor=tk.W)

    # Solution description
    solution_frame = tk.LabelFrame(
        main_frame,
        text="✅ The Solution (After)",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
        fg="#00aa00",
        padx=10,
        pady=10,
    )
    solution_frame.pack(fill=tk.X, pady=(0, 20))

    solution_text = tk.Label(
        solution_frame,
        text="• Switched to tk.Button with explicit color properties\n"
        "• Guaranteed high-contrast colors on all systems\n"
        "• Clear disabled states with proper visual feedback\n"
        "• Reliable hover effects and consistent appearance",
        font=("Arial", 10),
        bg="#f0f0f0",
        justify=tk.LEFT,
    )
    solution_text.pack(anchor=tk.W)

    # Interactive demo section
    demo_frame = tk.LabelFrame(
        main_frame,
        text="🖱️ Interactive Button Demo",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
        padx=15,
        pady=15,
    )
    demo_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

    # Demo instructions
    instructions = tk.Label(
        demo_frame,
        text="Click buttons to test functionality. Notice the high contrast and clear readability:",
        font=("Arial", 10),
        bg="#f0f0f0",
    )
    instructions.pack(pady=(0, 15))

    # Button examples with different states
    examples = [
        ("Boat B001", "normal", True, True, False),
        ("Boat B002", "running", False, True, True),
        ("Boat B003", "complete", True, False, True),
        ("Boat B004", "ready", True, False, False),
    ]

    # Header
    header_frame = tk.Frame(demo_frame, bg="#f0f0f0")
    header_frame.pack(fill=tk.X, pady=(0, 5))

    headers = ["Boat", "Status", "START", "STOP", "RESET"]
    for i, header in enumerate(headers):
        tk.Label(
            header_frame,
            text=header,
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            width=12 if i == 0 else 10,
        ).grid(row=0, column=i, padx=5)

    # Separator
    separator = tk.Frame(demo_frame, height=2, bg="#cccccc")
    separator.pack(fill=tk.X, pady=5)

    # Create example rows
    for boat, status, start_enabled, stop_enabled, reset_enabled in examples:
        row_frame = tk.Frame(demo_frame, bg="#f0f0f0")
        row_frame.pack(fill=tk.X, pady=2)

        # Boat label
        tk.Label(
            row_frame, text=boat, font=("Arial", 10, "bold"), bg="#f0f0f0", width=12
        ).grid(row=0, column=0, padx=5)

        # Status label with color coding
        status_colors = {
            "normal": "#0066cc",
            "running": "#cc0000",
            "complete": "#00aa00",
            "ready": "#0066cc",
        }
        status_texts = {
            "normal": "Ready",
            "running": "RUNNING",
            "complete": "✓ Complete",
            "ready": "Ready",
        }

        tk.Label(
            row_frame,
            text=status_texts[status],
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            fg=status_colors[status],
            width=10,
        ).grid(row=0, column=1, padx=5)

        # START button
        start_bg = "#4CAF50" if start_enabled else "#cccccc"
        start_fg = "white" if start_enabled else "#666666"
        start_btn = tk.Button(
            row_frame,
            text="START",
            bg=start_bg,
            fg=start_fg,
            activebackground="#45a049" if start_enabled else "#cccccc",
            activeforeground="white" if start_enabled else "#666666",
            font=("Arial", 9, "bold"),
            width=8,
            relief="raised",
            bd=2,
            state="normal" if start_enabled else "disabled",
            command=lambda b=boat: show_click_message("START", b),
        )
        start_btn.grid(row=0, column=2, padx=5)

        # STOP button
        stop_bg = "#f44336" if stop_enabled else "#cccccc"
        stop_fg = "white" if stop_enabled else "#666666"
        stop_btn = tk.Button(
            row_frame,
            text="STOP",
            bg=stop_bg,
            fg=stop_fg,
            activebackground="#da190b" if stop_enabled else "#cccccc",
            activeforeground="white" if stop_enabled else "#666666",
            font=("Arial", 9, "bold"),
            width=8,
            relief="raised",
            bd=2,
            state="normal" if stop_enabled else "disabled",
            command=lambda b=boat: show_click_message("STOP", b),
        )
        stop_btn.grid(row=0, column=3, padx=5)

        # RESET button
        reset_bg = "#e0e0e0" if reset_enabled else "#cccccc"
        reset_fg = "black" if reset_enabled else "#666666"
        reset_btn = tk.Button(
            row_frame,
            text="RESET",
            bg=reset_bg,
            fg=reset_fg,
            activebackground="#ddd" if reset_enabled else "#cccccc",
            activeforeground="black" if reset_enabled else "#666666",
            font=("Arial", 9, "bold"),
            width=8,
            relief="raised",
            bd=2,
            state="normal" if reset_enabled else "disabled",
            command=lambda b=boat: show_click_message("RESET", b),
        )
        reset_btn.grid(row=0, column=4, padx=5)

    # Color specifications
    specs_frame = tk.LabelFrame(
        main_frame,
        text="🎨 Color Specifications",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
        padx=10,
        pady=10,
    )
    specs_frame.pack(fill=tk.X, pady=(0, 20))

    specs_text = tk.Label(
        specs_frame,
        text="START: Green #4CAF50 background, white text\n"
        "STOP: Red #f44336 background, white text\n"
        "RESET: Gray #e0e0e0 background, black text\n"
        "DISABLED: Light gray #cccccc background, dark gray #666666 text\n"
        "HOVER: Darker shade of the base color for active feedback",
        font=("Arial", 10),
        bg="#f0f0f0",
        justify=tk.LEFT,
    )
    specs_text.pack(anchor=tk.W)

    # Bottom controls
    controls_frame = tk.Frame(main_frame, bg="#f0f0f0")
    controls_frame.pack(fill=tk.X)

    # Test message display
    global message_label
    message_label = tk.Label(
        controls_frame,
        text="Click any button to test functionality...",
        font=("Arial", 10),
        bg="#f0f0f0",
        fg="#666666",
    )
    message_label.pack(pady=(0, 10))

    # Close button
    close_btn = tk.Button(
        controls_frame,
        text="Close Demo",
        command=root.destroy,
        bg="#666666",
        fg="white",
        activebackground="#555555",
        activeforeground="white",
        font=("Arial", 11, "bold"),
        padx=20,
        relief="raised",
        bd=2,
    )
    close_btn.pack()

    return root


def show_click_message(action, boat):
    """Display click feedback message"""
    message = f"{action} clicked for {boat} - Button colors are working correctly!"
    message_label.config(text=message, fg="#00aa00")
    print(f"✅ {message}")


def main():
    """Run the button demo"""
    print("🎨 Starting Button Color Demo...")
    print("📋 This demo shows the solution to button visibility issues:")
    print("   • Reliable tk.Button colors instead of unreliable ttk.Button")
    print("   • High contrast guaranteed on all systems")
    print("   • Clear disabled states")
    print("   • Professional appearance")
    print()

    try:
        root = create_button_demo()
        print("✅ Demo window created successfully!")
        print("🖱️ Click buttons to test the color solution")
        print("📝 Check console for click confirmations")
        print()

        # Show initial status
        print("🎯 Button Color Specifications:")
        print("   • START: Green #4CAF50 with white text")
        print("   • STOP: Red #f44336 with white text")
        print("   • RESET: Gray #e0e0e0 with black text")
        print("   • DISABLED: Light gray #cccccc with dark gray text")
        print()

        root.mainloop()
        print("🏁 Button color demo completed!")

    except Exception as e:
        print(f"❌ Error running demo: {e}")
        return False

    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("✅ Button color solution is working perfectly!")
        print("🚀 Ready for race day with reliable, high-contrast buttons!")
    else:
        print("❌ Demo encountered issues.")

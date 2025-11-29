import json
import os
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


class RowingTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Rowing Event Timer")
        self.root.geometry("800x600")

        # Data storage
        self.participants = {}
        self.current_timers = {}
        self.data_file = "rowing_data.json"

        # Load existing data if available
        self.load_data()

        # Create GUI
        self.create_widgets()

    def create_widgets(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Registration Tab
        reg_frame = ttk.Frame(notebook)
        notebook.add(reg_frame, text="Registration")
        self.create_registration_tab(reg_frame)

        # Timing Tab
        timing_frame = ttk.Frame(notebook)
        notebook.add(timing_frame, text="Timing")
        self.create_timing_tab(timing_frame)

        # Results Tab
        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text="Results")
        self.create_results_tab(results_frame)

    def create_registration_tab(self, parent):
        # Registration form
        form_frame = ttk.LabelFrame(parent, text="Register Participant", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(form_frame, text="Boat Number:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.boat_number_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.boat_number_var, width=15).grid(
            row=0, column=1, sticky=tk.W, padx=(5, 20)
        )

        ttk.Label(form_frame, text="Participant Name:").grid(
            row=0, column=2, sticky=tk.W, pady=2
        )
        self.participant_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.participant_name_var, width=25).grid(
            row=0, column=3, sticky=tk.W, padx=5
        )

        ttk.Button(form_frame, text="Register", command=self.register_participant).grid(
            row=0, column=4, padx=10
        )

        # Participants list
        list_frame = ttk.LabelFrame(parent, text="Registered Participants", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Treeview for participants
        columns = ("Boat", "Name", "Run 1", "Run 2", "Status")
        self.participants_tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.participants_tree.heading(col, text=col)
            self.participants_tree.column(col, width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.participants_tree.yview
        )
        self.participants_tree.configure(yscrollcommand=scrollbar.set)

        self.participants_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(
            button_frame, text="Remove Selected", command=self.remove_participant
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="Clear All", command=self.clear_all_participants
        ).pack(side=tk.LEFT, padx=5)

    def create_timing_tab(self, parent):
        # Global run selection at the top
        run_select_frame = ttk.LabelFrame(parent, text="Current Run", padding=10)
        run_select_frame.pack(fill=tk.X, padx=10, pady=5)

        self.run_var = tk.StringVar(value="1")
        ttk.Label(
            run_select_frame,
            text="Select which run to time:",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            run_select_frame,
            text="Run 1",
            variable=self.run_var,
            value="1",
            command=self.update_all_boat_controls_for_run_change,
        ).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(
            run_select_frame,
            text="Run 2",
            variable=self.run_var,
            value="2",
            command=self.update_all_boat_controls_for_run_change,
        ).pack(side=tk.LEFT, padx=10)

        # Active timers display
        active_frame = ttk.LabelFrame(parent, text="Active Timers", padding=10)
        active_frame.pack(fill=tk.X, padx=10, pady=5)
        self.timer_display_frame = ttk.Frame(active_frame)
        self.timer_display_frame.pack(fill=tk.X)

        # Boat controls section
        self.boat_controls_frame = ttk.LabelFrame(
            parent, text="Boat Controls", padding=10
        )
        self.boat_controls_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Scrollable frame for boat controls
        self.boat_controls_canvas = tk.Canvas(self.boat_controls_frame)
        self.boat_controls_scrollbar = ttk.Scrollbar(
            self.boat_controls_frame,
            orient="vertical",
            command=self.boat_controls_canvas.yview,
        )
        self.boat_controls_inner_frame = ttk.Frame(self.boat_controls_canvas)

        self.boat_controls_inner_frame.bind(
            "<Configure>",
            lambda e: self.boat_controls_canvas.configure(
                scrollregion=self.boat_controls_canvas.bbox("all")
            ),
        )

        self.boat_controls_canvas.create_window(
            (0, 0), window=self.boat_controls_inner_frame, anchor="nw"
        )
        self.boat_controls_canvas.configure(
            yscrollcommand=self.boat_controls_scrollbar.set
        )

        self.boat_controls_canvas.pack(side="left", fill="both", expand=True)
        self.boat_controls_scrollbar.pack(side="right", fill="y")

        # Note: Using tk.Button instead of ttk.Button for reliable color control
        # ttk buttons can have theme conflicts with custom colors

        # Store boat control widgets for targeted updates
        self.boat_control_widgets = {}

        # Update displays
        self.update_timer_displays()
        self.update_boat_controls()

    def create_results_tab(self, parent):
        # Results display
        results_frame = ttk.LabelFrame(parent, text="Race Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Results treeview
        columns = (
            "Rank",
            "Boat",
            "Name",
            "Run 1",
            "Run 2",
            "Difference",
            "Consistency Score",
        )
        self.results_tree = ttk.Treeview(
            results_frame, columns=columns, show="headings", height=20
        )

        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100)

        # Scrollbar for results
        results_scrollbar = ttk.Scrollbar(
            results_frame, orient=tk.VERTICAL, command=self.results_tree.yview
        )
        self.results_tree.configure(yscrollcommand=results_scrollbar.set)

        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Control buttons
        results_button_frame = ttk.Frame(parent)
        results_button_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(
            results_button_frame,
            text="Calculate Results",
            command=self.calculate_results,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            results_button_frame, text="Export Results", command=self.export_results
        ).pack(side=tk.LEFT, padx=5)

    def register_participant(self):
        boat_number = self.boat_number_var.get().strip()
        name = self.participant_name_var.get().strip()

        if not boat_number or not name:
            messagebox.showerror(
                "Error", "Please enter both boat number and participant name."
            )
            return

        if boat_number in self.participants:
            messagebox.showerror("Error", f"Boat {boat_number} is already registered.")
            return

        # Add participant
        self.participants[boat_number] = {
            "name": name,
            "run1_time": None,
            "run2_time": None,
            "run1_start": None,
            "run2_start": None,
        }

        # Clear form
        self.boat_number_var.set("")
        self.participant_name_var.set("")

        # Update displays
        self.update_participants_display()
        self.update_boat_controls()
        self.save_data()

    def remove_participant(self):
        selection = self.participants_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a participant to remove.")
            return

        item = self.participants_tree.item(selection[0])
        boat_number = item["values"][0]

        if messagebox.askyesno("Confirm", f"Remove boat {boat_number}?"):
            del self.participants[boat_number]
            self.update_participants_display()
            self.update_boat_controls()
            self.save_data()

    def clear_all_participants(self):
        if messagebox.askyesno(
            "Confirm", "Clear all participants? This will delete all data."
        ):
            self.participants.clear()
            self.current_timers.clear()
            self.update_participants_display()
            self.update_boat_controls()
            self.update_timer_displays()
            self.save_data()

    def start_timer(self, boat=None):
        if boat is None:
            boat = getattr(self, "_current_boat", None)

        run = self.run_var.get()

        if not boat:
            messagebox.showerror("Error", "No boat specified.")
            return

        if boat not in self.participants:
            messagebox.showerror("Error", "Selected boat is not registered.")
            return

        timer_key = f"{boat}_run{run}"

        if timer_key in self.current_timers:
            messagebox.showwarning(
                "Warning", f"Timer for Boat {boat} Run {run} is already running."
            )
            return

        # Check if this run already has a time
        run_key = f"run{run}_time"
        if self.participants[boat][run_key] is not None:
            if not messagebox.askyesno(
                "Confirm",
                f"Boat {boat} Run {run} already has a time. Start new timing?",
            ):
                return

        # Start timer
        start_time = time.time()
        self.current_timers[timer_key] = {
            "start_time": start_time,
            "boat": boat,
            "run": run,
        }

        # Update participant data
        self.participants[boat][f"run{run}_start"] = start_time
        self.participants[boat][f"run{run}_time"] = None

        self.update_timer_displays()
        self.update_participants_display()
        self.update_single_boat_controls(boat)

    def stop_timer(self, boat=None):
        if boat is None:
            boat = getattr(self, "_current_boat", None)

        run = self.run_var.get()

        if not boat:
            messagebox.showerror("Error", "No boat specified.")
            return

        timer_key = f"{boat}_run{run}"

        if timer_key not in self.current_timers:
            messagebox.showwarning(
                "Warning", f"No active timer for Boat {boat} Run {run}."
            )
            return

        # Stop timer
        end_time = time.time()
        start_time = self.current_timers[timer_key]["start_time"]
        elapsed_time = end_time - start_time

        # Save time
        self.participants[boat][f"run{run}_time"] = elapsed_time

        # Remove from active timers
        del self.current_timers[timer_key]

        self.update_timer_displays()
        self.update_participants_display()
        self.update_single_boat_controls(boat)
        self.save_data()

    def start_timer_with_feedback(self, boat):
        """Start timer with visual feedback"""
        self.start_timer(boat)

    def stop_timer_with_feedback(self, boat):
        """Stop timer with visual feedback instead of popup"""
        run = self.run_var.get()
        timer_key = f"{boat}_run{run}"

        if timer_key in self.current_timers:
            # Get the elapsed time before stopping
            elapsed_time = time.time() - self.current_timers[timer_key]["start_time"]

            # Stop the timer
            self.stop_timer(boat)

            # Flash the status for visual feedback
            self.flash_completion_status(boat, run, elapsed_time)

    def flash_completion_status(self, boat, run, elapsed_time):
        """Provide visual feedback when timer is stopped"""
        # This will be handled by the improved status display in update_boat_controls
        # The status now shows a checkmark and time, providing immediate visual feedback
        pass

    def reset_timer(self, boat=None):
        if boat is None:
            boat = getattr(self, "_current_boat", None)

        run = self.run_var.get()

        if not boat:
            messagebox.showerror("Error", "No boat specified.")
            return

        timer_key = f"{boat}_run{run}"

        if timer_key in self.current_timers:
            if messagebox.askyesno(
                "Confirm", f"Reset active timer for Boat {boat} Run {run}?"
            ):
                del self.current_timers[timer_key]
                self.participants[boat][f"run{run}_time"] = None
                self.participants[boat][f"run{run}_start"] = None
                self.update_timer_displays()
                self.update_participants_display()
                self.update_single_boat_controls(boat)
        else:
            if messagebox.askyesno(
                "Confirm", f"Clear saved time for Boat {boat} Run {run}?"
            ):
                self.participants[boat][f"run{run}_time"] = None
                self.participants[boat][f"run{run}_start"] = None
                self.update_participants_display()
                self.update_single_boat_controls(boat)

    def update_timer_displays(self):
        # Clear existing displays
        for widget in self.timer_display_frame.winfo_children():
            widget.destroy()

        if not self.current_timers:
            ttk.Label(
                self.timer_display_frame, text="No active timers", font=("Arial", 12)
            ).pack()
            return

        # Create displays for active timers
        for timer_key, timer_data in self.current_timers.items():
            frame = ttk.Frame(self.timer_display_frame)
            frame.pack(fill=tk.X, pady=2)

            boat = timer_data["boat"]
            run = timer_data["run"]

            ttk.Label(
                frame, text=f"Boat {boat} Run {run}:", font=("Arial", 10, "bold")
            ).pack(side=tk.LEFT)

            timer_label = ttk.Label(
                frame, text="00:00.00", font=("Arial", 12), foreground="red"
            )
            timer_label.pack(side=tk.LEFT, padx=10)

            # Store reference for updating
            timer_data["label"] = timer_label

        # Schedule update
        self.root.after(10, self.update_running_timers)

    def update_running_timers(self):
        for timer_key, timer_data in self.current_timers.items():
            if "label" in timer_data:
                elapsed = time.time() - timer_data["start_time"]
                timer_data["label"].config(text=self.format_time(elapsed))

        if self.current_timers:
            self.root.after(10, self.update_running_timers)

    def update_participants_display(self):
        # Clear existing items
        for item in self.participants_tree.get_children():
            self.participants_tree.delete(item)

        # Add participants
        for boat_number, data in sorted(self.participants.items()):
            run1_display = (
                self.format_time(data["run1_time"]) if data["run1_time"] else "-"
            )
            run2_display = (
                self.format_time(data["run2_time"]) if data["run2_time"] else "-"
            )

            # Determine status
            status = "Registered"
            if data["run1_time"] and data["run2_time"]:
                status = "Complete"
            elif data["run1_time"] or data["run2_time"]:
                status = "Partial"

            self.participants_tree.insert(
                "",
                tk.END,
                values=(boat_number, data["name"], run1_display, run2_display, status),
            )

    def update_boat_controls(self):
        # Clear existing controls and widget references
        for widget in self.boat_controls_inner_frame.winfo_children():
            widget.destroy()
        self.boat_control_widgets = {}

        if not self.participants:
            ttk.Label(
                self.boat_controls_inner_frame,
                text="No registered participants. Go to Registration tab to add boats.",
                font=("Arial", 10),
            ).pack(pady=20)
            return

        # Get current run
        run = self.run_var.get()

        # Header
        header_frame = ttk.Frame(self.boat_controls_inner_frame)
        header_frame.pack(fill=tk.X, pady=5)

        ttk.Label(header_frame, text="Boat", font=("Arial", 10, "bold"), width=8).grid(
            row=0, column=0
        )
        ttk.Label(header_frame, text="Name", font=("Arial", 10, "bold"), width=20).grid(
            row=0, column=1
        )
        ttk.Label(
            header_frame, text="Status", font=("Arial", 10, "bold"), width=18
        ).grid(row=0, column=2)
        ttk.Label(
            header_frame, text="Current Time", font=("Arial", 10, "bold"), width=12
        ).grid(row=0, column=3)
        ttk.Label(
            header_frame, text="Controls", font=("Arial", 10, "bold"), width=25
        ).grid(row=0, column=4)

        # Separator
        ttk.Separator(self.boat_controls_inner_frame, orient=tk.HORIZONTAL).pack(
            fill=tk.X, pady=2
        )

        # Create controls for each boat
        for i, (boat, data) in enumerate(sorted(self.participants.items())):
            self._create_boat_control_row(boat, data, run)

    def _create_boat_control_row(self, boat, data, run):
        """Create a single boat control row and store widget references"""
        boat_frame = ttk.Frame(self.boat_controls_inner_frame)
        boat_frame.pack(fill=tk.X, pady=2, padx=5)

        # Boat number
        ttk.Label(boat_frame, text=boat, font=("Arial", 10, "bold"), width=8).grid(
            row=0, column=0, sticky=tk.W
        )

        # Participant name
        ttk.Label(boat_frame, text=data["name"], width=20).grid(
            row=0, column=1, sticky=tk.W
        )

        # Status label
        status_label = ttk.Label(boat_frame, width=18)
        status_label.grid(row=0, column=2, sticky=tk.W)

        # Time label
        time_label = ttk.Label(boat_frame, width=12, font=("Arial", 9, "bold"))
        time_label.grid(row=0, column=3, sticky=tk.W)

        # Control buttons
        button_frame = ttk.Frame(boat_frame)
        button_frame.grid(row=0, column=4, sticky=tk.W)

        # Start button
        start_btn = tk.Button(
            button_frame,
            text="START",
            command=lambda b=boat: self.start_timer_with_feedback(b),
            font=("Arial", 9, "bold"),
            width=8,
            relief="raised",
            bd=2,
        )
        start_btn.pack(side=tk.LEFT, padx=2)

        # Stop button
        stop_btn = tk.Button(
            button_frame,
            text="STOP",
            command=lambda b=boat: self.stop_timer_with_feedback(b),
            font=("Arial", 9, "bold"),
            width=8,
            relief="raised",
            bd=2,
        )
        stop_btn.pack(side=tk.LEFT, padx=2)

        # Reset button
        reset_btn = tk.Button(
            button_frame,
            text="RESET",
            command=lambda b=boat: self.reset_timer(b),
            font=("Arial", 9, "bold"),
            width=8,
            relief="raised",
            bd=2,
        )
        reset_btn.pack(side=tk.LEFT, padx=2)

        # Store widget references for targeted updates
        self.boat_control_widgets[boat] = {
            "status_label": status_label,
            "time_label": time_label,
            "start_btn": start_btn,
            "stop_btn": stop_btn,
            "reset_btn": reset_btn,
        }

        # Update this boat's display
        self._update_boat_row(boat, run)

    def _update_boat_row(self, boat, run):
        """Update a single boat's row without rebuilding the entire interface"""
        if boat not in self.boat_control_widgets:
            return

        widgets = self.boat_control_widgets[boat]
        data = self.participants.get(boat, {})
        timer_key = f"{boat}_run{run}"
        run_key = f"run{run}_time"

        # Update status and time display
        if timer_key in self.current_timers:
            status_text = f"RUNNING Run {run}"
            status_color = "red"
            status_font = ("Arial", 9, "bold")
            current_time = "TIMING..."
            time_color = "red"
        elif data.get(run_key) is not None:
            status_text = f"✓ Run {run}: {self.format_time(data[run_key])}"
            status_color = "green"
            status_font = ("Arial", 9, "bold")
            current_time = self.format_time(data[run_key])
            time_color = "green"
        else:
            status_text = f"Run {run} Ready"
            status_color = "blue"
            status_font = ("Arial", 9, "normal")
            current_time = "-"
            time_color = "black"

        # Update labels
        widgets["status_label"].config(
            text=status_text, foreground=status_color, font=status_font
        )
        widgets["time_label"].config(text=current_time, foreground=time_color)

        # Update button states and colors
        if timer_key in self.current_timers:
            # Timer is running
            widgets["start_btn"].config(state="disabled", bg="#cccccc", fg="#666666")
            widgets["stop_btn"].config(
                state="normal",
                bg="#f44336",
                fg="white",
                activebackground="#da190b",
                activeforeground="white",
            )
            widgets["reset_btn"].config(
                state="normal",
                bg="#e0e0e0",
                fg="black",
                activebackground="#ddd",
                activeforeground="black",
            )
        else:
            # Timer not running
            widgets["start_btn"].config(
                state="normal",
                bg="#4CAF50",
                fg="white",
                activebackground="#45a049",
                activeforeground="white",
            )
            widgets["stop_btn"].config(state="disabled", bg="#cccccc", fg="#666666")

            # Reset enabled only if there's a time to reset
            if data.get(run_key) is not None:
                widgets["reset_btn"].config(
                    state="normal",
                    bg="#e0e0e0",
                    fg="black",
                    activebackground="#ddd",
                    activeforeground="black",
                )
            else:
                widgets["reset_btn"].config(
                    state="disabled", bg="#cccccc", fg="#666666"
                )

    def update_single_boat_controls(self, boat):
        """Update only a specific boat's controls to avoid interface blinking"""
        if (
            not hasattr(self, "boat_control_widgets")
            or boat not in self.boat_control_widgets
        ):
            # Fallback to full update if widgets don't exist
            self.update_boat_controls()
            return

        run = self.run_var.get()
        self._update_boat_row(boat, run)

    def update_all_boat_controls_for_run_change(self):
        """Update all boat controls when run selection changes"""
        if not hasattr(self, "boat_control_widgets"):
            # No widgets exist yet, use full update
            self.update_boat_controls()
            return

        run = self.run_var.get()
        for boat in self.boat_control_widgets.keys():
            self._update_boat_row(boat, run)

    def calculate_results(self):
        # Clear existing results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Calculate results for participants with both runs
        results = []

        for boat, data in self.participants.items():
            if data["run1_time"] and data["run2_time"]:
                run1_time = data["run1_time"]
                run2_time = data["run2_time"]
                difference = abs(run1_time - run2_time)

                results.append(
                    {
                        "boat": boat,
                        "name": data["name"],
                        "run1_time": run1_time,
                        "run2_time": run2_time,
                        "difference": difference,
                    }
                )

        # Sort by consistency (smallest difference wins)
        results.sort(key=lambda x: x["difference"])

        # Display results
        for rank, result in enumerate(results, 1):
            self.results_tree.insert(
                "",
                tk.END,
                values=(
                    rank,
                    result["boat"],
                    result["name"],
                    self.format_time(result["run1_time"]),
                    self.format_time(result["run2_time"]),
                    self.format_time(result["difference"]),
                    f"{result['difference']:.3f}s",
                ),
            )

        if results:
            messagebox.showinfo(
                "Results",
                f"Results calculated for {len(results)} completed participants.",
            )
        else:
            messagebox.showwarning(
                "No Results", "No participants have completed both runs."
            )

    def export_results(self):
        if not self.results_tree.get_children():
            messagebox.showwarning("No Results", "Please calculate results first.")
            return

        try:
            filename = f"rowing_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, "w") as f:
                # Header
                f.write("Rank,Boat,Name,Run 1,Run 2,Difference,Consistency Score\n")

                # Data
                for item in self.results_tree.get_children():
                    values = self.results_tree.item(item)["values"]
                    f.write(",".join(str(v) for v in values) + "\n")

            messagebox.showinfo("Export Complete", f"Results exported to {filename}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results: {str(e)}")

    def format_time(self, seconds):
        if seconds is None:
            return "-"
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes:02d}:{secs:06.3f}"

    def save_data(self):
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.participants, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r") as f:
                    self.participants = json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            self.participants = {}


def main():
    root = tk.Tk()
    app = RowingTimer(root)

    # Update displays initially
    app.update_participants_display()
    app.update_boat_controls()

    root.mainloop()


if __name__ == "__main__":
    main()

import csv
import json
import os
import sys
import time
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk


class RowingTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Skelskør Roklub - Ro Konkurrence Timer")
        self.root.geometry("900x700")

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

        # Add club header
        header_frame = tk.Frame(self.root, bg="#1e3a8a", height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        # Club header content frame (centered)
        content_frame = tk.Frame(header_frame, bg="#1e3a8a")
        content_frame.pack(expand=True)

        # Try to load logo
        try:
            # Check for local file or PyInstaller bundled file
            logo_path = "club_logo.png"
            if hasattr(sys, "_MEIPASS"):
                logo_path = os.path.join(sys._MEIPASS, "club_logo.png")
            
            if os.path.exists(logo_path):
                self.logo_img = tk.PhotoImage(file=logo_path)
                logo_label = tk.Label(
                    content_frame, 
                    image=self.logo_img, 
                    bg="#1e3a8a"
                )
                logo_label.pack(side=tk.LEFT, padx=20)
        except Exception as e:
            print(f"Could not load logo: {e}")

        # Text frame
        text_frame = tk.Frame(content_frame, bg="#1e3a8a")
        text_frame.pack(side=tk.LEFT)

        # Club title
        title_label = tk.Label(
            text_frame,
            text="🚣 SKELSKØR ROKLUB 🚣",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1e3a8a",
        )
        title_label.pack(pady=(5, 0))

        # Subtitle
        subtitle_label = tk.Label(
            text_frame,
            text="Ro Konkurrence Timer • Gammelgade 25, 4230 Skælskør",
            font=("Arial", 10),
            fg="#bfdbfe",
            bg="#1e3a8a",
        )
        subtitle_label.pack(pady=(0, 5))

        # Registration Tab
        reg_frame = ttk.Frame(notebook)
        notebook.add(reg_frame, text="📝 Tilmeldinger")
        self.create_registration_tab(reg_frame)

        # Timing Tab
        timing_frame = ttk.Frame(notebook)
        notebook.add(timing_frame, text="⏱️ Tidtagning")
        self.create_timing_tab(timing_frame)

        # Results Tab
        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text="🏆 Resultater")
        self.create_results_tab(results_frame)

    def create_registration_tab(self, parent):
        # Registration form
        form_frame = ttk.LabelFrame(parent, text="🚣 Tilmeld Deltager", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(form_frame, text="Båd Nummer:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.boat_number_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.boat_number_var, width=15).grid(
            row=0, column=1, sticky=tk.W, padx=(5, 20)
        )

        ttk.Label(form_frame, text="Deltager Navn:").grid(
            row=0, column=2, sticky=tk.W, pady=2
        )
        self.participant_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.participant_name_var, width=25).grid(
            row=0, column=3, sticky=tk.W, padx=5
        )

        ttk.Button(
            form_frame, text="📝 Tilmeld", command=self.register_participant
        ).grid(row=0, column=4, padx=10)

        # Participants list
        list_frame = ttk.LabelFrame(parent, text="🚣 Tilmeldte Deltagere", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Treeview for participants
        columns = ("Båd", "Navn", "Tur 1", "Tur 2", "Status")
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
            button_frame, text="🗑️ Fjern Valgte", command=self.remove_participant
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="🧹 Ryd Alt", command=self.clear_all_participants
        ).pack(side=tk.LEFT, padx=5)

    def create_timing_tab(self, parent):
        # Global run selection at the top
        run_select_frame = ttk.LabelFrame(parent, text="🏁 Nuværende Tur", padding=10)
        run_select_frame.pack(fill=tk.X, padx=10, pady=5)

        self.run_var = tk.StringVar(value="1")
        ttk.Label(
            run_select_frame,
            text="Vælg hvilken tur der skal tages tid på:",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            run_select_frame,
            text="🥇 Tur 1",
            variable=self.run_var,
            value="1",
            command=self.update_all_boat_controls_for_run_change,
        ).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(
            run_select_frame,
            text="🥈 Tur 2",
            variable=self.run_var,
            value="2",
            command=self.update_all_boat_controls_for_run_change,
        ).pack(side=tk.LEFT, padx=10)

        # Boat controls section
        self.boat_controls_frame = ttk.LabelFrame(
            parent, text="🚣 Båd Kontroller", padding=10
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
        self.update_boat_controls()

    def create_results_tab(self, parent):
        # Results display
        results_frame = ttk.LabelFrame(
            parent, text="🏆 Konkurrence Resultater", padding=10
        )
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Results treeview
        columns = (
            "Plads",
            "Båd",
            "Navn",
            "Tur 1",
            "Tur 2",
            "Forskel",
            "Konsistens Score",
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
            text="🧮 Beregn Resultater",
            command=self.calculate_results,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            results_button_frame, text="📊 Eksporter CSV", command=self.export_csv
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            results_button_frame, text="📄 Eksporter PDF", command=self.export_pdf
        ).pack(side=tk.LEFT, padx=5)

    def register_participant(self):
        boat_number = self.boat_number_var.get().strip()
        name = self.participant_name_var.get().strip()

        if not boat_number or not name:
            messagebox.showerror(
                "Fejl", 
                "Indtast venligst både båd nummer og deltager navn.",
                parent=self.root
            )
            return

        if boat_number in self.participants:
            messagebox.showerror(
                "Fejl", 
                f"Båd {boat_number} er allerede tilmeldt.",
                parent=self.root
            )
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
            messagebox.showwarning(
                "Advarsel", 
                "Vælg venligst en deltager at fjerne.",
                parent=self.root
            )
            return

        item = self.participants_tree.item(selection[0])
        boat_number = str(item["values"][0])

        if messagebox.askyesno(
            "Bekræft", 
            f"Fjern båd {boat_number}?",
            parent=self.root
        ):
            del self.participants[boat_number]
            self.update_participants_display()
            self.update_boat_controls()
            self.save_data()

    def clear_all_participants(self):
        if messagebox.askyesno(
            "Bekræft", 
            "Ryd alle deltagere? Dette vil slette alle data.",
            parent=self.root
        ):
            try:
                self.participants.clear()
                self.current_timers.clear()
                self.update_participants_display()
                self.update_boat_controls()
                self.save_data()
            except Exception as e:
                messagebox.showerror(
                    "Fejl", 
                    f"Kunne ikke rydde deltagere: {e}",
                    parent=self.root
                )

    def start_timer(self, boat=None):
        if boat is None:
            boat = getattr(self, "_current_boat", None)

        run = self.run_var.get()

        if not boat:
            messagebox.showerror("Fejl", "Ingen båd specificeret.", parent=self.root)
            return

        if boat not in self.participants:
            messagebox.showerror("Fejl", "Valgte båd er ikke tilmeldt.", parent=self.root)
            return

        timer_key = f"{boat}_run{run}"

        if timer_key in self.current_timers:
            messagebox.showwarning(
                "Advarsel", 
                f"Timer for Båd {boat} Tur {run} kører allerede.",
                parent=self.root
            )
            return

        # Check if this run already has a time
        run_key = f"run{run}_time"
        if self.participants[boat][run_key] is not None:
            if not messagebox.askyesno(
                "Bekræft",
                f"Båd {boat} Tur {run} har allerede en tid. Start ny tidtagning?",
                parent=self.root
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

        self.update_participants_display()
        self.update_single_boat_controls(boat)

        # Start update loop if this is the first timer
        if len(self.current_timers) == 1:
            self.update_running_timers()

    def stop_timer(self, boat=None):
        if boat is None:
            boat = getattr(self, "_current_boat", None)

        run = self.run_var.get()

        if not boat:
            messagebox.showerror("Fejl", "Ingen båd specificeret.", parent=self.root)
            return

        timer_key = f"{boat}_run{run}"

        if timer_key not in self.current_timers:
            messagebox.showwarning(
                "Advarsel", 
                f"Ingen aktiv timer for Båd {boat} Tur {run}.",
                parent=self.root
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
            messagebox.showerror("Fejl", "Ingen båd specificeret.", parent=self.root)
            return

        timer_key = f"{boat}_run{run}"

        if timer_key in self.current_timers:
            if messagebox.askyesno(
                "Bekræft", 
                f"Nulstil aktiv timer for Båd {boat} Tur {run}?",
                parent=self.root
            ):
                del self.current_timers[timer_key]
                self.participants[boat][f"run{run}_time"] = None
                self.participants[boat][f"run{run}_start"] = None
                self.update_participants_display()
                self.update_single_boat_controls(boat)
        else:
            if messagebox.askyesno(
                "Bekræft", 
                f"Ryd gemt tid for Båd {boat} Tur {run}?",
                parent=self.root
            ):
                self.participants[boat][f"run{run}_time"] = None
                self.participants[boat][f"run{run}_start"] = None
                self.update_participants_display()
                self.update_single_boat_controls(boat)

    def update_running_timers(self):
        """Update the time display for all running timers"""
        run = self.run_var.get()
        
        for timer_key, timer_data in self.current_timers.items():
            boat = timer_data["boat"]
            # Only update if the timer belongs to the current run view
            if timer_data["run"] == run and boat in self.boat_control_widgets:
                elapsed = time.time() - timer_data["start_time"]
                time_str = self.format_time(elapsed)
                
                # Update the label in the boat control row
                self.boat_control_widgets[boat]["time_label"].config(
                    text=time_str, foreground="red"
                )

        if self.current_timers:
            self.root.after(50, self.update_running_timers)

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
            status = "Tilmeldt"
            if data["run1_time"] and data["run2_time"]:
                status = "Færdig"
            elif data["run1_time"] or data["run2_time"]:
                status = "Delvis"

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
                text="Ingen tilmeldte deltagere. Gå til Tilmeldinger for at tilføje både.",
                font=("Arial", 10),
            ).pack(pady=20)
            return

        # Get current run
        run = self.run_var.get()

        # Header
        header_frame = ttk.Frame(self.boat_controls_inner_frame)
        header_frame.pack(fill=tk.X, pady=5)

        ttk.Label(header_frame, text="Båd", font=("Arial", 10, "bold"), width=8).grid(
            row=0, column=0
        )
        ttk.Label(header_frame, text="Navn", font=("Arial", 10, "bold"), width=20).grid(
            row=0, column=1
        )
        ttk.Label(
            header_frame, text="Status", font=("Arial", 10, "bold"), width=18
        ).grid(row=0, column=2)
        ttk.Label(
            header_frame, text="Nuværende Tid", font=("Arial", 10, "bold"), width=12
        ).grid(row=0, column=3)
        ttk.Label(
            header_frame, text="Kontroller", font=("Arial", 10, "bold"), width=25
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
            status_text = f"🏃 KØRER Tur {run}"
            status_color = "red"
            status_font = ("Arial", 9, "bold")
            current_time = "TIDTAGER..."
            time_color = "red"
        elif data.get(run_key) is not None:
            status_text = f"✓ Tur {run}: {self.format_time(data[run_key])}"
            status_color = "green"
            status_font = ("Arial", 9, "bold")
            current_time = self.format_time(data[run_key])
            time_color = "green"
        else:
            status_text = f"🏁 Tur {run} Klar"
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
                "Resultater",
                f"Resultater beregnet for {len(results)} færdige deltagere.",
                parent=self.root
            )
        else:
            messagebox.showwarning(
                "Ingen Resultater", 
                "Ingen deltagere har gennemført begge ture.",
                parent=self.root
            )

    def export_csv(self):
        """Export results to CSV file with user-selected filename"""
        if not self.results_tree.get_children():
            messagebox.showwarning(
                "Ingen Resultater", 
                "Beregn venligst resultater først.",
                parent=self.root
            )
            return

        try:
            # Ask user for save location
            default_filename = (
                f"rowing_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=default_filename,
                title="Gem Resultater som CSV",
            )

            if not filename:  # User cancelled
                return

            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                # Header
                writer.writerow(
                    [
                        "Plads",
                        "Båd",
                        "Navn",
                        "Tur 1",
                        "Tur 2",
                        "Forskel",
                        "Konsistens Score",
                    ]
                )

                # Data
                for item in self.results_tree.get_children():
                    values = self.results_tree.item(item)["values"]
                    writer.writerow(values)

            messagebox.showinfo(
                "CSV Eksport Færdig", f"Resultater eksporteret til:\n{filename}"
            )

        except Exception as e:
            messagebox.showerror(
                "CSV Eksport Fejl", f"Kunne ikke eksportere CSV: {str(e)}"
            )

    def export_pdf(self):
        """Export results to PDF file with formatted layout"""
        if not self.results_tree.get_children():
            messagebox.showwarning(
                "Ingen Resultater", "Beregn venligst resultater først."
            )
            return

        try:
            # Try to import reportlab
            try:
                from reportlab.lib import colors
                from reportlab.lib.enums import TA_CENTER, TA_LEFT
                from reportlab.lib.pagesizes import A4
                from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
                from reportlab.lib.units import inch
                from reportlab.platypus import (
                    Paragraph,
                    SimpleDocTemplate,
                    Spacer,
                    Table,
                    TableStyle,
                )
            except ImportError:
                messagebox.showerror(
                    "PDF Eksport Fejl",
                    "PDF eksport kræver 'reportlab' biblioteket.\n\n"
                    + "Installer det med:\n"
                    + "pip install reportlab\n\n"
                    + "Brug i stedet CSV eksport indtil da.",
                )
                return

            # Ask user for save location
            default_filename = (
                f"rowing_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=default_filename,
                title="Gem Resultater som PDF",
            )

            if not filename:  # User cancelled
                return

            # Create PDF document
            doc = SimpleDocTemplate(
                filename,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18,
            )

            # Container for the 'Flowable' objects
            elements = []

            # Get styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "CustomTitle",
                parent=styles["Heading1"],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#2E4057"),
            )

            subtitle_style = ParagraphStyle(
                "CustomSubtitle",
                parent=styles["Normal"],
                fontSize=12,
                spaceAfter=20,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#666666"),
            )

            # Club header with logo placeholder
            club_header = Paragraph("🚣 SKELSKØR ROKLUB 🚣", title_style)
            elements.append(club_header)

            # Title
            title_text = "Ro Konkurrence Resultater"
            title = Paragraph(title_text, title_style)
            elements.append(title)

            # Event details
            event_info = (
                f"Genereret den {datetime.now().strftime('%d. %B %Y kl. %H:%M')}<br/>"
                f"Gammelgade 25, 4230 Skælskør • www.skelskoerroklub.dk"
            )
            subtitle = Paragraph(event_info, subtitle_style)
            elements.append(subtitle)
            elements.append(Spacer(1, 20))

            # Prepare table data
            table_data = [
                [
                    "Plads",
                    "Båd",
                    "Deltager Navn",
                    "Tur 1",
                    "Tur 2",
                    "Forskel",
                    "Score",
                ]
            ]

            for item in self.results_tree.get_children():
                values = self.results_tree.item(item)["values"]
                if values:
                    table_data.append(list(values))

            # Create table
            table = Table(
                table_data,
                colWidths=[
                    0.6 * inch,
                    0.7 * inch,
                    2.0 * inch,
                    0.9 * inch,
                    0.9 * inch,
                    0.9 * inch,
                    0.8 * inch,
                ],
            )

            # Table styling
            table.setStyle(
                TableStyle(
                    [
                        # Header row
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E4057")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        # Data rows
                        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 1), (-1, -1), 10),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [colors.beige, colors.white],
                        ),
                        ("ALIGN", (0, 1), (0, -1), "CENTER"),  # Rank column
                        ("ALIGN", (1, 1), (1, -1), "CENTER"),  # Boat column
                        ("ALIGN", (2, 1), (2, -1), "LEFT"),  # Name column
                        ("ALIGN", (3, 1), (-1, -1), "CENTER"),  # Time columns
                        # Grid
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        # Special styling for winner
                        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#FFD700")),
                        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
                    ]
                )
            )

            elements.append(table)
            elements.append(Spacer(1, 30))

            # Add summary information
            total_participants = len(table_data) - 1
            if total_participants > 0:
                winner_data = table_data[1]  # First data row after header
                winner_name = winner_data[2]
                winner_consistency = winner_data[6]

                summary_style = ParagraphStyle(
                    "Summary",
                    parent=styles["Normal"],
                    fontSize=11,
                    spaceAfter=10,
                    alignment=TA_LEFT,
                )

                summary_text = [
                    "<b>Konkurrence Sammendrag:</b>",
                    f"• Antal Deltagere: {total_participants}",
                    f"• Vinder: {winner_name} (Mest Konsistent)",
                    f"• Vinder Konsistens Score: {winner_consistency}",
                ]

                for text in summary_text:
                    if text:
                        elements.append(Paragraph(text, summary_style))
                    else:
                        elements.append(Spacer(1, 6))

            # Build PDF
            doc.build(elements)

            messagebox.showinfo(
                "PDF Eksport Færdig", f"Resultater eksporteret til:\n{filename}"
            )

        except Exception as e:
            messagebox.showerror(
                "PDF Eksport Fejl", f"Kunne ikke eksportere PDF: {str(e)}"
            )

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
            error_msg = f"Fejl ved gemning af data: {e}"
            print(error_msg)
            # Only show popup if root exists (might be during shutdown)
            if hasattr(self, "root") and self.root:
                messagebox.showerror(
                    "Gemmer Fejl", 
                    f"Kunne ikke gemme data!\n\nTjek filrettigheder.\n{e}",
                    parent=self.root
                )

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

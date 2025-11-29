#!/usr/bin/env python3
"""
Skelskør Roklub - Ro Konkurrence Timer med Eksempel Data
Dette script starter ro timer applikationen og indlæser valgfrit eksempel data til demonstration.
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
    """Opret eksempel data til demonstrations formål"""
    sample_data = {
        "B001": {
            "name": "Anders Sørensen",
            "run1_time": 65.234,
            "run2_time": 65.890,
            "run1_start": None,
            "run2_start": None,
        },
        "B002": {
            "name": "Birgitte Hansen",
            "run1_time": 62.123,
            "run2_time": 63.456,
            "run1_start": None,
            "run2_start": None,
        },
        "B003": {
            "name": "Christian Madsen",
            "run1_time": 68.567,
            "run2_time": 68.234,
            "run1_start": None,
            "run2_start": None,
        },
        "B004": {
            "name": "Dorthe Nielsen",
            "run1_time": 61.789,
            "run2_time": 64.123,
            "run1_start": None,
            "run2_start": None,
        },
        "B005": {
            "name": "Erik Petersen",
            "run1_time": 70.111,
            "run2_time": 70.222,
            "run1_start": None,
            "run2_start": None,
        },
        "B006": {
            "name": "Freja Andersen",
            "run1_time": 59.876,
            "run2_time": None,
            "run1_start": None,
            "run2_start": None,
        },
        "B007": {
            "name": "Gustav Larsen",
            "run1_time": None,
            "run2_time": None,
            "run1_start": None,
            "run2_start": None,
        },
    }
    return sample_data


def show_welcome_dialog():
    """Vis velkomst dialog med mulighed for at indlæse eksempel data"""
    root = tk.Tk()
    root.withdraw()  # Skjul hovedvinduet midlertidigt

    # Tjek om data fil eksisterer
    data_file = "rowing_data.json"
    has_existing_data = os.path.exists(data_file) and os.path.getsize(data_file) > 0

    if has_existing_data:
        message = (
            "Velkommen til Skelskør Roklub Ro Timer!\n\n"
            "Eksisterende data fundet. Applikationen vil indlæse din forrige session.\n\n"
            "Klik OK for at fortsætte med eksisterende data, eller Annuller for at afslutte."
        )

        result = messagebox.askokcancel("Skelskør Roklub - Eksisterende Data", message)
        root.destroy()
        return result, False
    else:
        message = (
            "Velkommen til Skelskør Roklub Ro Timer!\n\n"
            "Det ser ud til at være første gang du kører applikationen.\n\n"
            "Vil du indlæse eksempel data til demonstrations formål?\n\n"
            "Eksempel data inkluderer:\n"
            "• 7 tilmeldte deltagere\n"
            "• 5 med færdige tider (begge ture)\n"
            "• 1 med delvis data (kun én tur)\n"
            "• 1 uden registrerede tider\n\n"
            "Vælg 'Ja' for eksempel data, 'Nej' for tom start, eller 'Annuller' for at afslutte."
        )

        result = messagebox.askyesnocancel("Skelskør Roklub - Første Kørsel", message)
        root.destroy()

        if result is None:  # Cancel
            return False, False
        elif result is True:  # Yes - load sample data
            return True, True
        else:  # No - start empty
            return True, False


def load_sample_data(app):
    """Indlæs eksempel data i applikationen"""
    try:
        sample_data = create_sample_data()
        app.participants.update(sample_data)
        app.save_data()
        app.update_participants_display()
        app.update_boat_controls()

        # Vis info om indlæste data
        messagebox.showinfo(
            "Eksempel Data Indlæst",
            "Eksempel data er blevet indlæst!\n\n"
            "Tjek Tilmeldinger fanen for at se deltagere.\n"
            "Gå til Resultater fanen og klik 'Beregn Resultater' for at se placeringer.\n\n"
            "Du kan nu eksperimentere med tidtagnings funktionerne!",
        )
        return True

    except Exception as e:
        messagebox.showerror("Fejl", f"Kunne ikke indlæse eksempel data: {str(e)}")
        return False


def main():
    """Hoved funktion til at starte applikationen"""
    print("Starter Skelskør Roklub Timer Applikation...")

    # Vis velkomst dialog
    should_continue, load_sample = show_welcome_dialog()

    if not should_continue:
        print("Applikation afbrudt af bruger.")
        return

    try:
        # Opret hoved applikationen
        root = tk.Tk()
        app = RowingTimer(root)

        # Indlæs eksempel data hvis ønsket
        if load_sample:
            print("Indlæser eksempel data...")
            load_sample_data(app)

        # Opdater visninger indledningsvist
        app.update_participants_display()
        app.update_boat_controls()

        print("Applikation startet med succes!")
        print("Luk applikations vinduet for at afslutte.")

        # Start GUI event loop
        root.mainloop()

    except KeyboardInterrupt:
        print("\nApplikation afbrudt af bruger.")
    except Exception as e:
        print(f"Fejl ved kørsel af applikation: {e}")
        messagebox.showerror("Applikations Fejl", f"Der opstod en fejl: {str(e)}")


if __name__ == "__main__":
    main()

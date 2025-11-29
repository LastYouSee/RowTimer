#!/usr/bin/env python3
"""
Skelskør Roklub - Ro Konkurrence Timer Demo
Dette script demonstrerer det nye individuelle båd kontrolsystem.
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
            "name": "Skælskør Stolt",
            "run1_time": 67.234,
            "run2_time": None,
            "run1_start": None,
            "run2_start": None,
        },
        "B002": {
            "name": "Storebælt Storm",
            "run1_time": None,
            "run2_time": None,
            "run1_start": None,
            "run2_start": None,
        },
        "B003": {
            "name": "Vikinge Årer",
            "run1_time": 65.890,
            "run2_time": 66.123,
            "run1_start": None,
            "run2_start": None,
        },
        "B004": {
            "name": "Gammelgade Glider",
            "run1_time": None,
            "run2_time": None,
            "run1_start": None,
            "run2_start": None,
        },
        "B005": {
            "name": "Dansk Drage",
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
        "🚣‍♀️ SKELSKØR ROKLUB DEMO 🚣‍♂️\n\n"
        "Dette demo viser det NYE individuelle båd kontrolsystem!\n\n"
        "✨ VIGTIGSTE FORBEDRINGER:\n"
        "• Hver båd har dedikerede START/STOP/RESET knapper\n"
        "• Ingen dropdown menu nødvendig længere\n"
        "• Perfekt til timing af flere både samtidig\n"
        "• Visuelle status indikatorer for hver båd\n"
        "• Hurtigere betjening under tætte starts\n\n"
        "📋 DEMO DATA INKLUDERER:\n"
        "• B001 Skælskør Stolt (Tur 1 færdig)\n"
        "• B002 Storebælt Storm (klar til timing)\n"
        "• B003 Vikinge Årer (begge ture færdige)\n"
        "• B004 Gammelgade Glider (klar til timing)\n"
        "• B005 Dansk Drage (Tur 1 færdig)\n\n"
        "🎯 PRØV DISSE FUNKTIONER:\n"
        "1. Gå til Tidtagning fanen for at se båd kontroller\n"
        "2. Skift mellem Tur 1 og Tur 2 tilstande\n"
        "3. Start/stop timere for forskellige både\n"
        "4. Tjek Resultater fanen for placeringer\n\n"
        "Klar til at starte demoen?"
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
            "Demo Klar!",
            "🎉 Demo data indlæst med succes!\n\n"
            "📍 NÆSTE TRIN:\n"
            "1. Tjek Tilmeldinger fanen for at se alle både\n"
            "2. Gå til Tidtagning fanen for at se det nye interface\n"
            "3. Prøv at tage tid på både B002 og B004\n"
            "4. Færdiggør Tur 2 for både B001 og B005\n"
            "5. Beregn resultater for at se placeringer!\n\n"
            "💡 TIP: Du kan tage tid på flere både samtidig\n"
            "ved at klikke på forskellige bådes START knapper!",
        )

        return True

    except Exception as e:
        messagebox.showerror("Demo Error", f"Failed to setup demo: {str(e)}")
        return False


def main():
    """Main demo function"""
    print("🚣‍♀️ Starter Skelskør Roklub Demo...")

    # Show introduction
    if not show_demo_dialog():
        print("Demo afbrudt af bruger.")
        return

    try:
        # Create the application
        root = tk.Tk()
        app = RowingTimer(root)

        # Setup demo data
        if not setup_demo_app(app):
            return

        print("✅ Demo startet med succes!")
        print("🎯 Prøv de nye individuelle båd kontroller i Tidtagning fanen!")
        print("📝 Luk applikations vinduet når du er færdig.")

        # Add demo title to window
        root.title("Skelskør Roklub - DEMO TILSTAND (Nye Båd Kontroller)")

        # Start the GUI
        root.mainloop()

    except KeyboardInterrupt:
        print("\n⏹️ Demo afbrudt af bruger.")
    except Exception as e:
        print(f"❌ Demo fejl: {e}")
        messagebox.showerror("Demo Fejl", f"Der opstod en fejl: {str(e)}")


if __name__ == "__main__":
    main()

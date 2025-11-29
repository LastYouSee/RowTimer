#!/usr/bin/env python3
"""
Skelskør Roklub - Ro Konkurrence Timer Opstart
Dette script starter ro timer applikationen med klubbens branding og logo.
"""

import os
import sys
import time

# Tilføj nuværende mappe til Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def show_club_logo():
    """Vis Skelskør Roklub logo og velkomst besked"""
    logo = """
╔══════════════════════════════════════════════════════════════╗
║                    🚣 SKELSKØR ROKLUB 🚣                    ║
║                                                              ║
║        🚣‍♂️    ~~~~~~~~~~~~~~~~~~~~~~~~    🚣‍♀️              ║
║             ~~~~     ROKLUB     ~~~~                        ║
║                 ~~~~~~~~~~~~~~~~                             ║
║                                                              ║
║    Grundlagt med passion for roning og fællesskab           ║
║              Gammelgade 25, 4230 Skælskør                   ║
║               www.skelskoerroklub.dk                         ║
║               Tel: +45 40 73 16 60                          ║
║                                                              ║
║  "Sammen på vandet - sammen i fællesskabet"                 ║
╚══════════════════════════════════════════════════════════════╝

    ⚓ SKELSKØR ROKLUB - SIDEN GRUNDLÆGGELSEN ⚓
         Motionsroning • Coastal • Kajak • Inrigger
              Effektiv motion i smukke omgivelser

═══════════════════════════════════════════════════════════════
           🏁 RO KONKURRENCE TIMER SYSTEM 🏁
═══════════════════════════════════════════════════════════════

    Professionel tidtagning til rokonkurrencer
    ✅ Individuelle båd kontroller
    ✅ Samtidige timer funktioner
    ✅ Konsistens-baseret rangering
    ✅ CSV og PDF eksport muligheder
    ✅ Dansk interface og branding

═══════════════════════════════════════════════════════════════
"""
    print(logo)


def check_dependencies():
    """Tjek om nødvendige afhængigheder er tilgængelige"""
    print("🔍 Tjekker systemkrav...")

    # Tjek Python version
    if sys.version_info.major < 3 or sys.version_info.minor < 6:
        print("❌ Python 3.6 eller højere påkrævet")
        print(
            f"   Nuværende version: {sys.version_info.major}.{sys.version_info.minor}"
        )
        return False

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} OK")

    # Tjek tkinter
    try:
        import tkinter

        print("✅ tkinter GUI framework OK")
    except ImportError:
        print("❌ tkinter ikke tilgængelig")
        print("   På Linux: sudo apt-get install python3-tk")
        return False

    # Tjek rowing_timer modul
    try:
        from rowing_timer import RowingTimer

        print("✅ Skelskør Roklub Timer modul OK")
    except ImportError as e:
        print(f"❌ Kunne ikke importere rowing_timer: {e}")
        print("   Sørg for at rowing_timer.py er i samme mappe")
        return False

    # Tjek ReportLab (valgfrit)
    try:
        import reportlab

        print("✅ ReportLab PDF eksport OK")
        pdf_available = True
    except ImportError:
        print("⚠️ ReportLab ikke installeret - kun CSV eksport tilgængelig")
        print("   Installer med: pip install reportlab")
        pdf_available = False

    return True, pdf_available


def main():
    """Hoved funktion til at starte Skelskør Roklub Timer"""
    # Vis klub logo
    show_club_logo()

    print("🚀 Starter Skelskør Roklub Ro Konkurrence Timer...")
    print()

    # Tjek afhængigheder
    deps_ok, pdf_ok = check_dependencies()

    if not deps_ok:
        print("\n❌ Systemkrav ikke opfyldt. Kan ikke starte applikationen.")
        input("\nTryk Enter for at afslutte...")
        return False

    print()
    print("🎯 Alle systemkrav opfyldt!")

    if not pdf_ok:
        print("💡 Tip: Installer ReportLab for PDF eksport funktionalitet")

    print("\n" + "=" * 50)
    print("           STARTER APPLIKATION...")
    print("=" * 50)

    try:
        # Import og start hovedapplikationen
        import tkinter as tk

        from rowing_timer import RowingTimer

        # Opret hovedvindue
        root = tk.Tk()

        # Opret applikation
        app = RowingTimer(root)

        # Opdater displays indledningsvist
        app.update_participants_display()
        app.update_boat_controls()

        print("✅ Skelskør Roklub Timer startet med succes!")
        print("📝 Luk applikations vinduet for at afslutte")
        print()
        print("🚣 God konkurrence og held og lykke! 🚣")

        # Start GUI
        root.mainloop()

        print("\n👋 Skelskør Roklub Timer afsluttet")
        print("   Tak fordi du brugte vores system!")

        return True

    except KeyboardInterrupt:
        print("\n\n⏹️ Applikation afbrudt af bruger")
        return False

    except Exception as e:
        print(f"\n❌ Fejl ved start af applikation: {e}")
        print("\nDetaljer:")
        import traceback

        traceback.print_exc()
        print("\n🔧 Prøv at:")
        print("   1. Genstart applikationen")
        print("   2. Tjek at alle filer er tilstede")
        print("   3. Kontakt support hvis problemet fortsætter")
        input("\nTryk Enter for at afslutte...")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 Uventet fejl: {e}")
        input("\nTryk Enter for at afslutte...")
        sys.exit(1)

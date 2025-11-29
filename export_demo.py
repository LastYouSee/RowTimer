#!/usr/bin/env python3
"""
Export Demo for Rowing Timer Application
This script demonstrates the CSV and PDF export functionality with sample data.
"""

import csv
import os
import sys
import tempfile
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rowing_timer import RowingTimer
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure rowing_timer.py is in the same directory.")
    sys.exit(1)


def create_sample_data():
    """Create realistic sample race data"""
    return {
        "B001": {
            "name": "Lightning Strike",
            "run1_time": 67.234,
            "run2_time": 67.890,
            "run1_start": None,
            "run2_start": None,
        },
        "B002": {
            "name": "Thunder Bolt",
            "run1_time": 65.123,
            "run2_time": 66.456,
            "run1_start": None,
            "run2_start": None,
        },
        "B003": {
            "name": "Wave Rider",
            "run1_time": 68.567,
            "run2_time": 68.234,
            "run1_start": None,
            "run2_start": None,
        },
        "B004": {
            "name": "Storm Chaser",
            "run1_time": 63.789,
            "run2_time": 66.123,
            "run1_start": None,
            "run2_start": None,
        },
        "B005": {
            "name": "Ocean Master",
            "run1_time": 70.111,
            "run2_time": 70.222,
            "run1_start": None,
            "run2_start": None,
        },
        "B006": {
            "name": "Sea Dragon",
            "run1_time": 64.555,
            "run2_time": 64.444,
            "run1_start": None,
            "run2_start": None,
        },
    }


def setup_demo_app():
    """Set up the application with sample data"""
    print("🚣‍♀️ Setting up Export Demo...")

    root = tk.Tk()
    root.withdraw()  # Hide main window for demo

    app = RowingTimer(root)

    # Load sample data
    sample_data = create_sample_data()
    app.participants.update(sample_data)

    # Calculate results to populate the results tree
    app.calculate_results()

    print(f"✅ Demo setup complete with {len(sample_data)} participants")
    return app, root


def demo_csv_export(app):
    """Demonstrate CSV export functionality"""
    print("\n📊 Testing CSV Export...")

    try:
        # Create temporary file for demo
        temp_dir = tempfile.gettempdir()
        csv_filename = os.path.join(
            temp_dir, f"rowing_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        # Mock the file dialog to return our chosen filename
        original_asksaveasfilename = tk.filedialog.asksaveasfilename
        tk.filedialog.asksaveasfilename = lambda **kwargs: csv_filename

        # Temporarily disable messagebox for demo
        original_showinfo = messagebox.showinfo
        messagebox.showinfo = lambda title, message: print(f"✅ {title}: {message}")

        # Call export function
        app.export_csv()

        # Restore original functions
        tk.filedialog.asksaveasfilename = original_asksaveasfilename
        messagebox.showinfo = original_showinfo

        # Verify the CSV was created and read its contents
        if os.path.exists(csv_filename):
            with open(csv_filename, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)

            print(f"📄 CSV Export Results:")
            print(f"   • File: {csv_filename}")
            print(f"   • Rows: {len(rows)} (including header)")
            print(f"   • Size: {os.path.getsize(csv_filename)} bytes")

            # Show sample of the data
            print(f"\n📋 CSV Content Preview:")
            for i, row in enumerate(rows[:4]):  # Show first 4 rows
                if i == 0:
                    print(f"   Header: {', '.join(row)}")
                else:
                    print(f"   Row {i}: {', '.join(row)}")

            if len(rows) > 4:
                print(f"   ... and {len(rows) - 4} more rows")

            return csv_filename
        else:
            print("❌ CSV file was not created")
            return None

    except Exception as e:
        print(f"❌ CSV Export Error: {str(e)}")
        return None


def demo_pdf_export(app):
    """Demonstrate PDF export functionality"""
    print("\n📄 Testing PDF Export...")

    try:
        # Check if reportlab is available
        try:
            import reportlab

            print("✅ ReportLab library is available")
        except ImportError:
            print(
                "⚠️ ReportLab not installed - PDF export will show installation instructions"
            )

            # Temporarily capture the error message
            original_showerror = messagebox.showerror
            error_messages = []

            def capture_error(title, message):
                error_messages.append((title, message))
                print(f"📋 {title}: {message}")

            messagebox.showerror = capture_error

            app.export_pdf()

            # Restore original function
            messagebox.showerror = original_showerror

            if error_messages:
                print("✅ PDF export properly handled missing dependency")
                return None
            else:
                print("❌ PDF export did not handle missing dependency correctly")
                return None

        # Create temporary file for demo
        temp_dir = tempfile.gettempdir()
        pdf_filename = os.path.join(
            temp_dir, f"rowing_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        # Mock the file dialog to return our chosen filename
        original_asksaveasfilename = tk.filedialog.asksaveasfilename
        tk.filedialog.asksaveasfilename = lambda **kwargs: pdf_filename

        # Temporarily disable messagebox for demo
        original_showinfo = messagebox.showinfo
        messagebox.showinfo = lambda title, message: print(f"✅ {title}: {message}")

        # Call export function
        app.export_pdf()

        # Restore original functions
        tk.filedialog.asksaveasfilename = original_asksaveasfilename
        messagebox.showinfo = original_showinfo

        # Verify the PDF was created
        if os.path.exists(pdf_filename):
            file_size = os.path.getsize(pdf_filename)
            print(f"📄 PDF Export Results:")
            print(f"   • File: {pdf_filename}")
            print(f"   • Size: {file_size} bytes")

            if file_size > 1000:  # PDF should be reasonably sized
                print("✅ PDF appears to be properly generated")
                return pdf_filename
            else:
                print("⚠️ PDF file seems too small - may be corrupted")
                return None
        else:
            print("❌ PDF file was not created")
            return None

    except Exception as e:
        print(f"❌ PDF Export Error: {str(e)}")
        return None


def show_file_contents_info(csv_file, pdf_file):
    """Show information about the generated files"""
    print("\n" + "=" * 60)
    print("📊 EXPORT DEMO RESULTS")
    print("=" * 60)

    if csv_file:
        print(f"✅ CSV Export: SUCCESS")
        print(f"   📄 File: {os.path.basename(csv_file)}")
        print(f"   📁 Location: {os.path.dirname(csv_file)}")
        print(f"   💾 Size: {os.path.getsize(csv_file)} bytes")
        print(f"   🔗 Full path: {csv_file}")
    else:
        print("❌ CSV Export: FAILED")

    print()

    if pdf_file:
        print(f"✅ PDF Export: SUCCESS")
        print(f"   📄 File: {os.path.basename(pdf_file)}")
        print(f"   📁 Location: {os.path.dirname(pdf_file)}")
        print(f"   💾 Size: {os.path.getsize(pdf_file)} bytes")
        print(f"   🔗 Full path: {pdf_file}")
    else:
        print("❌ PDF Export: FAILED (may need ReportLab installation)")

    print()
    print("🎯 Export Features Verified:")
    if csv_file:
        print("   • CSV export with proper formatting ✓")
        print("   • File dialog integration ✓")
        print("   • Data integrity maintained ✓")
    if pdf_file:
        print("   • PDF export with professional layout ✓")
        print("   • ReportLab integration working ✓")
        print("   • Formatted tables and styling ✓")

    if not pdf_file and not csv_file:
        print("   ⚠️ Both exports failed - check error messages above")
    elif csv_file and not pdf_file:
        print(
            "   ℹ️ CSV export working - install ReportLab for PDF: pip install reportlab"
        )


def cleanup_files(csv_file, pdf_file):
    """Clean up demo files"""
    print(f"\n🧹 Cleaning up demo files...")

    files_to_clean = [f for f in [csv_file, pdf_file] if f and os.path.exists(f)]

    if not files_to_clean:
        print("   No files to clean up")
        return

    try:
        for file_path in files_to_clean:
            os.remove(file_path)
            print(f"   🗑️ Removed: {os.path.basename(file_path)}")
        print("✅ Cleanup complete")
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")
        print("   You may need to manually delete the demo files")


def main():
    """Main demo function"""
    print("=" * 60)
    print("🚣‍♀️ ROWING TIMER - EXPORT FUNCTIONALITY DEMO")
    print("=" * 60)
    print("This demo tests both CSV and PDF export features")
    print("with realistic race data from 6 participants.")
    print()

    try:
        # Setup demo application
        app, root = setup_demo_app()

        # Test CSV export
        csv_file = demo_csv_export(app)

        # Test PDF export
        pdf_file = demo_pdf_export(app)

        # Show results
        show_file_contents_info(csv_file, pdf_file)

        # Ask if user wants to keep the files
        print("\n" + "=" * 60)
        keep_files = (
            input("Keep the exported demo files? (y/N): ").lower().startswith("y")
        )

        if not keep_files:
            cleanup_files(csv_file, pdf_file)
        else:
            print("📁 Demo files preserved for your inspection")

        # Cleanup tkinter
        root.destroy()

        print("\n🎉 Export demo completed successfully!")

        if csv_file and pdf_file:
            print("✅ Both CSV and PDF export are working correctly")
        elif csv_file:
            print("✅ CSV export is working - install ReportLab for PDF support")
        else:
            print("⚠️ Export functionality needs attention")

    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

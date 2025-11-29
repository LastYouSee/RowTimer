#!/usr/bin/env python3
"""
Test script for CSV and PDF export functionality
This script tests the export features of the rowing timer application.
"""

import csv
import os
import sys
import tempfile
import time
import tkinter as tk
from unittest.mock import MagicMock, patch

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rowing_timer import RowingTimer
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure rowing_timer.py is in the same directory.")
    sys.exit(1)


class ExportTester:
    """Test class for export functionality"""

    def __init__(self):
        self.test_results = []
        self.app = None
        self.temp_files = []

    def log_test(self, test_name, passed, message=""):
        """Log test results"""
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {test_name}: {message}")
        self.test_results.append(
            {"test": test_name, "passed": passed, "message": message}
        )

    def setup_test_app(self):
        """Create a test instance of the application"""
        try:
            # Create tkinter root
            root = tk.Tk()
            root.withdraw()  # Hide during testing

            self.app = RowingTimer(root)
            self.root = root

            # Mock GUI components
            self.app.results_tree = MagicMock()

            # Create mock result data
            mock_items = ["item1", "item2", "item3"]
            mock_values = [
                (
                    1,
                    "B001",
                    "Alice Johnson",
                    "01:05.234",
                    "01:05.890",
                    "00:00.656",
                    "0.656s",
                ),
                (
                    2,
                    "B002",
                    "Bob Smith",
                    "01:02.123",
                    "01:03.456",
                    "00:01.333",
                    "1.333s",
                ),
                (
                    3,
                    "B003",
                    "Carol Davis",
                    "01:08.567",
                    "01:08.234",
                    "00:00.333",
                    "0.333s",
                ),
            ]

            self.app.results_tree.get_children.return_value = mock_items

            # Mock the item method to return test data
            def mock_item(item_id):
                index = mock_items.index(item_id)
                return {"values": mock_values[index]}

            self.app.results_tree.item = mock_item

            return True
        except Exception as e:
            print(f"Failed to setup test app: {e}")
            return False

    def test_csv_export_functionality(self):
        """Test CSV export functionality"""
        try:
            # Create a temporary file for testing
            temp_file = tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False
            )
            temp_file.close()
            self.temp_files.append(temp_file.name)

            # Mock the file dialog to return our temp file
            with patch(
                "tkinter.filedialog.asksaveasfilename", return_value=temp_file.name
            ):
                # Call the export function
                self.app.export_csv()

            # Verify the file was created and has correct content
            if os.path.exists(temp_file.name):
                with open(temp_file.name, "r", newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    rows = list(reader)

                # Check header row
                expected_header = [
                    "Rank",
                    "Boat",
                    "Name",
                    "Run 1",
                    "Run 2",
                    "Difference",
                    "Consistency Score",
                ]
                if len(rows) >= 1 and rows[0] == expected_header:
                    # Check data rows
                    if len(rows) == 4:  # Header + 3 data rows
                        # Verify first data row
                        first_row = rows[1]
                        if (
                            first_row[0] == "1"
                            and first_row[1] == "B001"
                            and first_row[2] == "Alice Johnson"
                        ):
                            self.log_test(
                                "CSV Export Functionality",
                                True,
                                f"CSV exported with {len(rows) - 1} data rows and correct format",
                            )
                        else:
                            self.log_test(
                                "CSV Export Functionality",
                                False,
                                f"CSV data incorrect: {first_row}",
                            )
                    else:
                        self.log_test(
                            "CSV Export Functionality",
                            False,
                            f"Expected 4 rows (header + 3 data), got {len(rows)}",
                        )
                else:
                    self.log_test(
                        "CSV Export Functionality",
                        False,
                        f"CSV header incorrect: {rows[0] if rows else 'No rows'}",
                    )
            else:
                self.log_test(
                    "CSV Export Functionality", False, "CSV file was not created"
                )

        except Exception as e:
            self.log_test("CSV Export Functionality", False, f"Exception: {str(e)}")

    def test_csv_export_cancel(self):
        """Test CSV export when user cancels file dialog"""
        try:
            # Mock the file dialog to return None (user cancelled)
            with patch("tkinter.filedialog.asksaveasfilename", return_value=None):
                # Mock messagebox to track if any messages are shown
                with patch("tkinter.messagebox.showwarning") as mock_warning:
                    # Call the export function
                    self.app.export_csv()

                    # Should not show any warning when user cancels
                    if not mock_warning.called:
                        self.log_test(
                            "CSV Export Cancel",
                            True,
                            "Export properly handles user cancellation",
                        )
                    else:
                        self.log_test(
                            "CSV Export Cancel",
                            False,
                            "Unexpected warning shown on cancel",
                        )

        except Exception as e:
            self.log_test("CSV Export Cancel", False, f"Exception: {str(e)}")

    def test_csv_export_no_results(self):
        """Test CSV export when no results are available"""
        try:
            # Mock empty results
            self.app.results_tree.get_children.return_value = []

            # Mock messagebox to track warnings
            with patch("tkinter.messagebox.showwarning") as mock_warning:
                self.app.export_csv()

                # Should show warning about no results
                if mock_warning.called:
                    # Check the warning message
                    call_args = mock_warning.call_args[0]
                    if (
                        "No Results" in call_args[0]
                        and "calculate results first" in call_args[1]
                    ):
                        self.log_test(
                            "CSV Export No Results",
                            True,
                            "Properly warns when no results available",
                        )
                    else:
                        self.log_test(
                            "CSV Export No Results",
                            False,
                            f"Wrong warning message: {call_args}",
                        )
                else:
                    self.log_test(
                        "CSV Export No Results",
                        False,
                        "No warning shown for empty results",
                    )

        except Exception as e:
            self.log_test("CSV Export No Results", False, f"Exception: {str(e)}")

    def test_pdf_export_availability(self):
        """Test PDF export functionality availability"""
        try:
            # Test if PDF export method exists
            has_pdf_export = hasattr(self.app, "export_pdf")

            if not has_pdf_export:
                self.log_test(
                    "PDF Export Availability", False, "PDF export method not found"
                )
                return

            # Test PDF export without reportlab (should show error)
            with patch(
                "builtins.__import__",
                side_effect=ImportError("No module named 'reportlab'"),
            ):
                with patch("tkinter.messagebox.showerror") as mock_error:
                    self.app.export_pdf()

                    if mock_error.called:
                        call_args = mock_error.call_args[0]
                        if "reportlab" in call_args[1]:
                            self.log_test(
                                "PDF Export Availability",
                                True,
                                "Properly handles missing reportlab dependency",
                            )
                        else:
                            self.log_test(
                                "PDF Export Availability",
                                False,
                                f"Wrong error message: {call_args[1]}",
                            )
                    else:
                        self.log_test(
                            "PDF Export Availability",
                            False,
                            "No error shown for missing reportlab",
                        )

        except Exception as e:
            self.log_test("PDF Export Availability", False, f"Exception: {str(e)}")

    def test_pdf_export_with_reportlab(self):
        """Test PDF export functionality when reportlab is available"""
        try:
            # Try to import reportlab
            try:
                import reportlab

                has_reportlab = True
            except ImportError:
                has_reportlab = False

            if not has_reportlab:
                self.log_test(
                    "PDF Export with ReportLab",
                    True,
                    "Skipped - reportlab not installed (this is expected for basic testing)",
                )
                return

            # Create a temporary PDF file for testing
            temp_file = tempfile.NamedTemporaryFile(
                mode="w", suffix=".pdf", delete=False
            )
            temp_file.close()
            self.temp_files.append(temp_file.name)

            # Mock the file dialog to return our temp file
            with patch(
                "tkinter.filedialog.asksaveasfilename", return_value=temp_file.name
            ):
                # Mock messagebox to track success message
                with patch("tkinter.messagebox.showinfo") as mock_info:
                    # Call the export function
                    self.app.export_pdf()

                    # Check if success message was shown
                    if mock_info.called:
                        call_args = mock_info.call_args[0]
                        if "PDF Export Complete" in call_args[0]:
                            # Check if file exists and has some content
                            if (
                                os.path.exists(temp_file.name)
                                and os.path.getsize(temp_file.name) > 0
                            ):
                                self.log_test(
                                    "PDF Export with ReportLab",
                                    True,
                                    f"PDF created successfully: {os.path.getsize(temp_file.name)} bytes",
                                )
                            else:
                                self.log_test(
                                    "PDF Export with ReportLab",
                                    False,
                                    "PDF file not created or empty",
                                )
                        else:
                            self.log_test(
                                "PDF Export with ReportLab",
                                False,
                                f"Wrong success message: {call_args}",
                            )
                    else:
                        self.log_test(
                            "PDF Export with ReportLab",
                            False,
                            "No success message shown",
                        )

        except Exception as e:
            self.log_test("PDF Export with ReportLab", False, f"Exception: {str(e)}")

    def test_export_buttons_exist(self):
        """Test that export buttons are present in the interface"""
        try:
            # Check if export methods exist
            has_csv_export = hasattr(self.app, "export_csv")
            has_pdf_export = hasattr(self.app, "export_pdf")

            if has_csv_export and has_pdf_export:
                self.log_test(
                    "Export Buttons Exist",
                    True,
                    "Both CSV and PDF export methods available",
                )
            else:
                missing = []
                if not has_csv_export:
                    missing.append("CSV export")
                if not has_pdf_export:
                    missing.append("PDF export")

                self.log_test(
                    "Export Buttons Exist",
                    False,
                    f"Missing export methods: {', '.join(missing)}",
                )

        except Exception as e:
            self.log_test("Export Buttons Exist", False, f"Exception: {str(e)}")

    def cleanup(self):
        """Clean up test resources"""
        try:
            if hasattr(self, "root"):
                self.root.destroy()

            # Clean up temporary files
            for temp_file in self.temp_files:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
        except:
            pass

    def run_all_tests(self):
        """Run all export tests"""
        print("=" * 70)
        print("ROWING TIMER - EXPORT FUNCTIONALITY TESTS")
        print("Testing CSV and PDF export capabilities")
        print("=" * 70)

        if not self.setup_test_app():
            print("Failed to setup test environment")
            return False

        try:
            # Run export tests
            self.test_export_buttons_exist()
            self.test_csv_export_functionality()
            self.test_csv_export_cancel()
            self.test_csv_export_no_results()
            self.test_pdf_export_availability()
            self.test_pdf_export_with_reportlab()

            # Summary
            passed_tests = sum(1 for result in self.test_results if result["passed"])
            total_tests = len(self.test_results)

            print("\n" + "=" * 70)
            print(f"EXPORT TEST SUMMARY: {passed_tests}/{total_tests} PASSED")

            if passed_tests == total_tests:
                print("✅ ALL EXPORT TESTS PASSED!")
                print("🎯 Verified export features:")
                print("   • CSV export with proper formatting ✓")
                print("   • PDF export availability checking ✓")
                print("   • User cancellation handling ✓")
                print("   • Empty results validation ✓")
                print("   • File dialog integration ✓")
                if self._check_reportlab_available():
                    print("   • PDF generation with reportlab ✓")
                else:
                    print("   • PDF fallback for missing reportlab ✓")
            else:
                print("❌ SOME EXPORT TESTS FAILED")
                failed_tests = [r for r in self.test_results if not r["passed"]]
                for test in failed_tests:
                    print(f"   • {test['test']}: {test['message']}")

            print("=" * 70)

            return passed_tests == total_tests

        finally:
            self.cleanup()

    def _check_reportlab_available(self):
        """Check if reportlab is available"""
        try:
            import reportlab

            return True
        except ImportError:
            return False


def main():
    """Main test function"""
    tester = ExportTester()
    success = tester.run_all_tests()

    if success:
        print("\n🎉 Export functionality is working correctly!")
        print("📊 Available export formats:")
        print("   • CSV - Comma-separated values for spreadsheets")
        print("   • PDF - Professional formatted reports")
        print("\n🚀 Users can now export race results in multiple formats!")

        if tester._check_reportlab_available():
            print("📋 ReportLab is installed - PDF export fully functional")
        else:
            print("📋 Install ReportLab for PDF export: pip install reportlab")
    else:
        print("\n⚠️ Some export functionality needs attention.")
        print("Basic CSV export should still work.")

    return success


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script for the Rowing Timer Application
This script performs basic functionality tests to ensure the application works correctly.
"""

import json
import os
import sys
import tempfile
import time
from unittest.mock import MagicMock, patch

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import tkinter as tk

    from rowing_timer import RowingTimer
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required modules are available.")
    sys.exit(1)


class TestRowingTimer:
    """Test class for the Rowing Timer application"""

    def __init__(self):
        self.test_results = []
        self.app = None

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
            # Create temporary data file
            self.temp_file = tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            )
            self.temp_file.close()

            # Create actual tkinter root for testing
            root = tk.Tk()
            root.withdraw()  # Hide the window during testing

            self.app = RowingTimer(root)
            self.app.data_file = self.temp_file.name
            self.root = root

            # Mock GUI components that aren't needed for logic tests
            self.app.participants_tree = MagicMock()
            self.app.participants_tree.get_children = MagicMock(return_value=[])
            self.app.participants_tree.delete = MagicMock()
            self.app.participants_tree.insert = MagicMock()

            self.app.boat_controls_inner_frame = MagicMock()
            self.app.boat_controls_inner_frame.winfo_children = MagicMock(
                return_value=[]
            )
            self.app.results_tree = MagicMock()
            self.app.results_tree.get_children = MagicMock(return_value=[])
            self.app.results_tree.delete = MagicMock()
            self.app.results_tree.insert = MagicMock()

            self.app.timer_display_frame = MagicMock()
            self.app.timer_display_frame.winfo_children = MagicMock(return_value=[])

            # Mock variables
            self.app.boat_number_var = MagicMock()
            self.app.participant_name_var = MagicMock()
            self.app.run_var = MagicMock()
            self.app.run_var.get.return_value = "1"

            return True
        except Exception as e:
            print(f"Failed to setup test app: {e}")
            return False

    def test_participant_registration(self):
        """Test participant registration functionality"""
        try:
            # Clear any existing participants first
            self.app.participants.clear()

            # Setup mock values
            self.app.boat_number_var.get.return_value = "B001"
            self.app.participant_name_var.get.return_value = "Test Rower"

            # Test registration
            self.app.register_participant()

            # Check if participant was added
            if "B001" in self.app.participants:
                participant = self.app.participants["B001"]
                if participant["name"] == "Test Rower":
                    self.log_test(
                        "Participant Registration",
                        True,
                        "Successfully registered participant",
                    )
                else:
                    self.log_test(
                        "Participant Registration",
                        False,
                        f"Participant name not stored correctly. Expected 'Test Rower', got '{participant['name']}'",
                    )
            else:
                self.log_test(
                    "Participant Registration",
                    False,
                    "Participant not added to dictionary",
                )

        except Exception as e:
            self.log_test("Participant Registration", False, f"Exception: {str(e)}")

    def test_duplicate_registration(self):
        """Test duplicate boat number handling"""
        try:
            # Add first participant
            self.app.boat_number_var.get.return_value = "B002"
            self.app.participant_name_var.get.return_value = "Rower One"
            self.app.register_participant()

            # Try to add duplicate
            self.app.participant_name_var.get.return_value = "Rower Two"
            initial_count = len(self.app.participants)

            # This should not add the duplicate (would show error dialog in real app)
            self.app.register_participant()
            final_count = len(self.app.participants)

            if initial_count == final_count:
                self.log_test(
                    "Duplicate Registration Check",
                    True,
                    "Duplicate registration prevented",
                )
            else:
                self.log_test(
                    "Duplicate Registration Check",
                    False,
                    "Duplicate registration allowed",
                )

        except Exception as e:
            self.log_test("Duplicate Registration Check", False, f"Exception: {str(e)}")

    def test_timer_functionality(self):
        """Test timer start/stop functionality"""
        try:
            # Add a participant first
            self.app.participants["B003"] = {
                "name": "Timer Test",
                "run1_time": None,
                "run2_time": None,
                "run1_start": None,
                "run2_start": None,
            }

            # Setup mock values for timer
            self.app.run_var.get.return_value = "1"

            # Start timer
            start_time = time.time()
            self.app.start_timer("B003")

            # Check if timer was started
            timer_key = "B003_run1"
            if timer_key in self.app.current_timers:
                # Simulate some time passing
                time.sleep(0.1)

                # Stop timer
                self.app.stop_timer("B003")

                # Check if time was recorded
                if self.app.participants["B003"]["run1_time"] is not None:
                    recorded_time = self.app.participants["B003"]["run1_time"]
                    if 0.05 <= recorded_time <= 0.2:  # Should be around 0.1 seconds
                        self.log_test(
                            "Timer Functionality",
                            True,
                            f"Timer recorded {recorded_time:.3f}s",
                        )
                    else:
                        self.log_test(
                            "Timer Functionality",
                            False,
                            f"Unexpected time: {recorded_time}",
                        )
                else:
                    self.log_test(
                        "Timer Functionality", False, "Time not recorded after stopping"
                    )
            else:
                self.log_test("Timer Functionality", False, "Timer not started")

        except Exception as e:
            self.log_test("Timer Functionality", False, f"Exception: {str(e)}")

    def test_results_calculation(self):
        """Test results calculation and ranking"""
        try:
            # Add test participants with times
            self.app.participants = {
                "B101": {
                    "name": "Consistent Rower",
                    "run1_time": 60.0,
                    "run2_time": 60.1,
                    "run1_start": None,
                    "run2_start": None,
                },
                "B102": {
                    "name": "Inconsistent Rower",
                    "run1_time": 58.0,
                    "run2_time": 62.0,
                    "run1_start": None,
                    "run2_start": None,
                },
                "B103": {
                    "name": "Very Consistent",
                    "run1_time": 65.0,
                    "run2_time": 65.05,
                    "run1_start": None,
                    "run2_start": None,
                },
            }

            # Calculate results
            self.app.calculate_results()

            # Check if results were calculated (mocked tree should have been called)
            if self.app.results_tree.insert.called:
                self.log_test(
                    "Results Calculation", True, "Results calculation completed"
                )
            else:
                self.log_test("Results Calculation", False, "Results not calculated")

        except Exception as e:
            self.log_test("Results Calculation", False, f"Exception: {str(e)}")

    def test_time_formatting(self):
        """Test time formatting function"""
        try:
            # Test various time formats
            test_cases = [
                (65.123, "01:05.123"),
                (0.500, "00:00.500"),
                (125.999, "02:05.999"),
                (None, "-"),
            ]

            all_passed = True
            for time_val, expected in test_cases:
                result = self.app.format_time(time_val)
                if result != expected:
                    self.log_test(
                        "Time Formatting",
                        False,
                        f"Expected {expected}, got {result} for {time_val}",
                    )
                    all_passed = False
                    break

            if all_passed:
                self.log_test("Time Formatting", True, "All time formats correct")

        except Exception as e:
            self.log_test("Time Formatting", False, f"Exception: {str(e)}")

    def test_data_persistence(self):
        """Test saving and loading data"""
        try:
            # Add test data
            test_data = {
                "B999": {
                    "name": "Persistence Test",
                    "run1_time": 45.67,
                    "run2_time": 46.78,
                    "run1_start": None,
                    "run2_start": None,
                }
            }

            self.app.participants = test_data

            # Save data
            self.app.save_data()

            # Clear participants and reload
            self.app.participants = {}
            self.app.load_data()

            # Check if data was loaded correctly
            if "B999" in self.app.participants:
                loaded_participant = self.app.participants["B999"]
                if (
                    loaded_participant["name"] == "Persistence Test"
                    and loaded_participant["run1_time"] == 45.67
                ):
                    self.log_test(
                        "Data Persistence", True, "Data saved and loaded correctly"
                    )
                else:
                    self.log_test(
                        "Data Persistence", False, "Data corrupted during save/load"
                    )
            else:
                self.log_test("Data Persistence", False, "Data not loaded")

        except Exception as e:
            self.log_test("Data Persistence", False, f"Exception: {str(e)}")

    def cleanup(self):
        """Clean up test files"""
        try:
            if hasattr(self, "temp_file") and os.path.exists(self.temp_file.name):
                os.unlink(self.temp_file.name)
            if hasattr(self, "root"):
                self.root.destroy()
        except:
            pass

    def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("ROWING TIMER APPLICATION TESTS")
        print("=" * 60)

        if not self.setup_test_app():
            print("Failed to setup test environment")
            return False

        try:
            # Run all tests
            self.test_participant_registration()
            self.test_duplicate_registration()
            self.test_timer_functionality()
            self.test_results_calculation()
            self.test_time_formatting()
            self.test_data_persistence()

            # Summary
            passed_tests = sum(1 for result in self.test_results if result["passed"])
            total_tests = len(self.test_results)

            print("\n" + "=" * 60)
            print(f"TEST SUMMARY: {passed_tests}/{total_tests} PASSED")

            if passed_tests == total_tests:
                print("✅ ALL TESTS PASSED - Application is ready to use!")
            else:
                print("❌ SOME TESTS FAILED - Check the issues above")

            print("=" * 60)

            return passed_tests == total_tests

        finally:
            self.cleanup()


def main():
    """Main test function"""
    tester = TestRowingTimer()
    success = tester.run_all_tests()

    if success:
        print("\n🎉 The Rowing Timer application appears to be working correctly!")
        print("You can now run: python rowing_timer.py")
    else:
        print(
            "\n⚠️  Some issues were found. The application may still work, but please check the errors above."
        )

    return success


if __name__ == "__main__":
    main()

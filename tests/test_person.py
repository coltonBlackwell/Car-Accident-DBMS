import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from car_crash_DB.entities.person import Person

class TestPerson(unittest.TestCase):

    def test_save_to_db(self):
        mock_cursor = MagicMock()
        person = Person(driver_id=1, name="Colton", address="123 Main St")

        person.save_to_db(mock_cursor)

        mock_cursor.execute.assert_called_once_with("""
            INSERT INTO customers (driver_id, name, address)
            VALUES (%s, %s, %s)
        """, (1, "Colton", "123 Main St"))
        print("✅ test_save_to_db passed")

    def test_remove_record(self):
        mock_cursor = MagicMock()

        # Simulate licenses returned for the driver
        mock_cursor.fetchall.side_effect = [
            [(123,), (456,)],  # licenses for driver_id
            [(10,), (11,)],    # reports for license 123
            [(12,)],           # reports for license 456
        ]

        Person.remove_record(mock_cursor, 1)

        expected_calls = [
            # Fetch licenses
            (("SELECT license FROM cars WHERE driver_id = %s", (1,)),),
            # Fetch report numbers for license 123
            (("SELECT report_number FROM car_accidents WHERE license = %s", (123,)),),
            # Delete from car_accidents for license 123
            (("DELETE FROM car_accidents WHERE license = %s", (123,)),),
            # Fetch report numbers for license 456
            (("SELECT report_number FROM car_accidents WHERE license = %s", (456,)),),
            # Delete from car_accidents for license 456
            (("DELETE FROM car_accidents WHERE license = %s", (456,)),),
            # Delete cars
            (("DELETE FROM cars WHERE driver_id = %s", (1,)),),
            # Delete accidents (set includes 10, 11, 12)
            (("DELETE FROM accidents WHERE report_number = %s", (10,)),),
            (("DELETE FROM accidents WHERE report_number = %s", (11,)),),
            (("DELETE FROM accidents WHERE report_number = %s", (12,)),),
            # Delete person
            (("DELETE FROM customers WHERE driver_id = %s", (1,)),),
        ]

        actual_calls = mock_cursor.execute.call_args_list
        for expected_call in expected_calls:
            self.assertIn(expected_call, actual_calls)

        self.assertEqual(mock_cursor.execute.call_count, len(expected_calls))
        print("✅ test_remove_record passed")

    def test_str_method(self):
        person = Person(1, "Colton", "123 Main St")
        self.assertEqual(str(person), "1 - Colton - 123 Main St")
        print("✅ test_str_method passed")

if __name__ == "__main__":
    unittest.main()

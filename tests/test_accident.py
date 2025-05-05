import sys
import os
import unittest
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from car_crash_DB.entities.accident import Accident

class TestAccident(unittest.TestCase):

    def test_initialization(self):
        acc = Accident(101, "Downtown", "2025-05-05")
        self.assertEqual(acc.report_number, 101)
        self.assertEqual(acc.location, "Downtown")
        self.assertEqual(acc.date, "2025-05-05")

    def test_str_representation(self):
        acc = Accident(202, "Main St", "2025-01-01")
        expected_str = "202 - Main St - 2025-01-01"
        self.assertEqual(str(acc), expected_str)

    def test_save_to_db_executes_correct_query(self):
        mock_cursor = MagicMock()
        acc = Accident(303, "Bridge Ave", "2025-03-15")
        acc.save_to_db(mock_cursor)

        mock_cursor.execute.assert_called_once_with("""
            INSERT INTO accidents (report_number, location, date)
            VALUES (%s, %s, %s)
        """, (303, "Bridge Ave", "2025-03-15"))


if __name__ == '__main__':
    unittest.main()
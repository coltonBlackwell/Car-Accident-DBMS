import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from car_crash_DB.entities.filesystem import FileSystem

class TestFileSystem(unittest.TestCase):

    @patch("car_crash_DB.entities.filesystem.mysql.connector.connect")
    def test_init_creates_database_and_connects(self, mock_connect):
        mock_temp_db = MagicMock()
        mock_main_db = MagicMock()
        mock_connect.side_effect = [mock_temp_db, mock_main_db]

        fs = FileSystem()

        self.assertEqual(mock_connect.call_count, 2)
        mock_temp_db.cursor.assert_called_once()
        mock_main_db.cursor.assert_called_once()
        print("✅ test_init_creates_database_and_connects passed")

    @patch("car_crash_DB.entities.filesystem.mysql.connector.connect")
    def test_create_person_table(self, mock_connect):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        fs = FileSystem()
        # Clear prior calls from __init__
        mock_cursor.reset_mock()
        mock_db.commit.reset_mock()

        fs.create_person_table()

        mock_cursor.execute.assert_called_once()
        mock_db.commit.assert_called_once()
        self.assertIn("CREATE TABLE IF NOT EXISTS customers", mock_cursor.execute.call_args[0][0])
        print("✅ test_create_person_table passed")

    @patch("car_crash_DB.entities.filesystem.mysql.connector.connect")
    def test_clear_all_tables(self, mock_connect):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        fs = FileSystem()
        mock_cursor.reset_mock()
        mock_db.commit.reset_mock()

        fs.clear_all_tables()

        calls = [call[0][0] for call in mock_cursor.execute.call_args_list]
        self.assertEqual(len(calls), 4)
        self.assertIn("DELETE FROM car_accidents", calls[0])
        self.assertIn("DELETE FROM accidents", calls[1])
        self.assertIn("DELETE FROM cars", calls[2])
        self.assertIn("DELETE FROM customers", calls[3])
        mock_db.commit.assert_called_once()
        print("✅ test_clear_all_tables passed")

if __name__ == "__main__":
    unittest.main()

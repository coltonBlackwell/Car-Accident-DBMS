import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from car_crash_DB.entities.car import Car

class MockCursor:
    def __init__(self):
        self.queries = []

    def execute(self, query, params):
        self.queries.append((query.strip(), params))

class TestCar(unittest.TestCase):
    def test_init(self):
        car = Car(1234, "Toyota", 2020, 1)
        self.assertEqual(car.license, 1234)
        self.assertEqual(car.model, "Toyota")
        self.assertEqual(car.year, 2020)
        self.assertEqual(car.driver_id, 1)

    def test_save_to_db(self):
        mock_cursor = MockCursor()
        car = Car(5678, "Honda", 2019, 2)
        car.save_to_db(mock_cursor)

        expected_query = """
            INSERT INTO cars (license, model, year, driver_id)
            VALUES (%s, %s, %s, %s)
        """.strip()
        self.assertIn((expected_query, (5678, "Honda", 2019, 2)), mock_cursor.queries)

    def test_link_to_accident(self):
        mock_cursor = MockCursor()
        car = Car(9876, "Ford", 2021, 3)
        car.link_to_accident(mock_cursor, 42)

        expected_query = """
            INSERT INTO car_accidents (report_number, license)
            VALUES (%s, %s)
        """.strip()
        self.assertIn((expected_query, (42, 9876)), mock_cursor.queries)

if __name__ == "__main__":
    unittest.main()
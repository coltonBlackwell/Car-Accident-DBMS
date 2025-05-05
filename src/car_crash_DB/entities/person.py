class Person:

    def __init__(self, driver_id, name, address):
        self.driver_id = driver_id
        self.name = name
        self.address = address

    def save_to_db(self, db_cursor):
        db_cursor.execute("""
            INSERT INTO customers (driver_id, name, address)
            VALUES (%s, %s, %s)
        """, (self.driver_id, self.name, self.address))

    @staticmethod
    def remove_record(db_cursor, driver_id):

        db_cursor.execute("SELECT license FROM cars WHERE driver_id = %s", (driver_id,))
        licenses = db_cursor.fetchall()

        report_numbers = set()
        for (license,) in licenses:
            db_cursor.execute("SELECT report_number FROM car_accidents WHERE license = %s", (license,))
            linked_reports = db_cursor.fetchall()
            for (report,) in linked_reports:
                report_numbers.add(report)

            db_cursor.execute("DELETE FROM car_accidents WHERE license = %s", (license,))

        db_cursor.execute("DELETE FROM cars WHERE driver_id = %s", (driver_id,))

        for report_number in report_numbers:
            db_cursor.execute("DELETE FROM accidents WHERE report_number = %s", (report_number,))

        db_cursor.execute("DELETE FROM customers WHERE driver_id = %s", (driver_id,))


    def __str__(self):
        return f"{self.driver_id} - {self.name} - {self.address}"
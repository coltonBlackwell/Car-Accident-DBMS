class Car:
    def __init__(self, license, model, year, driver_id):
        self.license = license
        self.model = model
        self.year = year
        self.driver_id = driver_id

    def save_to_db(self, db_cursor):
        db_cursor.execute("""
            INSERT INTO cars (license, model, year, driver_id)
            VALUES (%s, %s, %s, %s)
        """, (self.license, self.model, self.year, self.driver_id))

    def link_to_accident(self, db_cursor, report_number):
        db_cursor.execute("""
            INSERT INTO car_accidents (report_number, license)
            VALUES (%s, %s)
        """, (report_number, self.license))

    def __str__(self):
        return f"{self.license} - {self.model} - {self.year}"
class Accident:
    def __init__(self, report_number, location, date):
        self.report_number = report_number
        self.location = location
        self.date = date

    def save_to_db(self, db_cursor):
        db_cursor.execute("""
            INSERT INTO accidents (report_number, location, date)
            VALUES (%s, %s, %s)
        """, (self. report_number, self.location, self.date))

    def __str__(self):
        return f"{self.report_number} - {self.location} - {self.date}"
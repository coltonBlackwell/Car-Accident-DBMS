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

    def __str__(self):
        return f"{self.driver_id} - {self.name} - {self.address}"
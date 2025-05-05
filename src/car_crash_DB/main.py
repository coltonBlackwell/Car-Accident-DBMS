import mysql.connector
import os

class FileSystem: 
    def __init__(self):
        temp_db = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST", "localhost"),
            user="colton",
            password=os.environ.get("MYSQL_PASSWORD", "good4Colton!")
        )
        temp_cursor = temp_db.cursor()
        temp_cursor.execute("CREATE DATABASE IF NOT EXISTS car_accidents")
        temp_db.close()

        self.mydb = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST", "localhost"),
            user="colton",
            password=os.environ.get("MYSQL_PASSWORD", "good4Colton!"),
            database=os.environ.get("MYSQL_DB", "car_accidents")
        )
        self.mycursor = self.mydb.cursor()
        print("Connected to DB:", self.mydb)

    def create_person_table(self):
        self.mycursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                driver_id INT PRIMARY KEY,
                name VARCHAR(255),
                address VARCHAR(255)
            )
        """)
        self.mydb.commit()

    def create_cars_table(self):
        self.mycursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                license INT PRIMARY KEY, 
                model VARCHAR(255),
                year INT
            )        
        """)
        self.mydb.commit()

    def create_accidents_table(self):
        self.mycursor.execute("""
            CREATE TABLE IF NOT EXISTS accidents (
                report_number INT PRIMARY KEY, 
                location VARCHAR(255),
                date DATE
            )        
        """)
        self.mydb.commit()
        
    
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

    
class Car:
    def __init__(self, license, model, year):
        self.license = license
        self.model = model
        self.year = year

    def save_to_db(self, db_cursor):
        db_cursor.execute("""
            INSERT INTO cars (license, model, year)
            VALUES (%s, %s, %s)
        """, (self.license, self.model, self.year))

    def __str__(self):
        return f"{self.license} - {self.model} - {self.year}"
    
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

def main():

    fs = FileSystem()
    fs.create_person_table()
    fs.create_cars_table()
    fs.create_accidents_table()

    # colton = Person(21, "Colton", "422 montroyal Blvd.")
    # colton.save_to_db(fs.mycursor)
    # fs.mydb.commit()
    # print("Person saved:", colton)

    # camero = Car(11111, "Camero", 2025)
    # camero.save_to_db(fs.mycursor)
    # fs.mydb.commit()
    # print("Car saved: ", camero)

    head_on_collision = Accident(212, "Edgemont Village", '2010-08-11')
    head_on_collision.save_to_db(fs.mycursor)
    fs.mydb.commit()
    print("Accident reported: ", head_on_collision)


if __name__ == '__main__':
    main()
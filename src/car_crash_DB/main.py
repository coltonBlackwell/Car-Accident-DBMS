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
        
class Person:

    def __init__(self, driver_id, name, address):
        self.driver_id = driver_id
        self.name = name
        self.address = address

        mycursor = mydb.cursor()

        mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")



    def __str__(self):
        return f"{self.driver_id} - {self.name} - {self.address}"
    
class Car:
    def __init__(self, license, model, year):
        self.license = license
        self.model = model
        self.year = year

    def __str__(self):
        return f"{self.license} - {self.model} - {self.year}"
    
class Accident:
    def __init__(self, report_number, location, date):
        self.report_number = report_number
        self.location = location
        self.date = date

    def __str__(self):
        return f"{self.report_number} - {self.location} - {self.date}"

def main():
    colton = Person(21, "Colton", "422 montroyal Blvd.")
    print(colton)


if __name__ == '__main__':
    main()
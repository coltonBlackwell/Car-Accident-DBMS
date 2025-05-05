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
                year INT, 
                driver_id INT, 
                FOREIGN KEY (driver_id) REFERENCES customers(driver_id)
                    ON DELETE CASCADE
            )        
        """)
        self.mydb.commit()

    def create_car_accidents_table(self):
        self.mycursor.execute("""
            CREATE TABLE IF NOT EXISTS car_accidents (
                report_number INT,
                license INT,
                PRIMARY KEY (report_number, license),
                FOREIGN KEY (report_number) REFERENCES accidents(report_number)
                    ON DELETE CASCADE,
                FOREIGN KEY (license) REFERENCES cars(license)
                    ON DELETE CASCADE
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

    def drop_database(self, db_name="car_accidents"):
        temp_db = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST", "localhost"),
            user="colton",
            password=os.environ.get("MYSQL_PASSWORD", "good4Colton!")
        )
        temp_cursor = temp_db.cursor()
        temp_cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        temp_db.close()
        print(f"Database '{db_name}' dropped.")

    def clear_all_tables(self):
        try:
            self.mycursor.execute("DELETE FROM car_accidents")
            self.mycursor.execute("DELETE FROM accidents")
            self.mycursor.execute("DELETE FROM cars")
            self.mycursor.execute("DELETE FROM customers")
            self.mydb.commit()
            print("All records deleted from all tables.")
        except Exception as e:
            self.mydb.rollback()
            print(f"Error clearing tables: {e}")
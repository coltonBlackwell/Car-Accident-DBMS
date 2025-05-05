from entities import Person, FileSystem, Car, Accident 
from flask import Flask, request, render_template

app = Flask(__name__)

fs = FileSystem()

fs.create_person_table()
fs.create_cars_table()
fs.create_accidents_table()
fs.create_car_accidents_table()



@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        if "submit_all" in request.form:
            try:
                # Person info
                driver_id = int(request.form.get("person_driver_id"))
                name = request.form.get("person_name")
                address = request.form.get("person_address")
                person = Person(driver_id, name, address)
                person.save_to_db(fs.mycursor)
                fs.mydb.commit()

                # Car info
                license = int(request.form.get("car_license"))
                model = request.form.get("car_model")
                year = int(request.form.get("car_year"))
                car = Car(license, model, year, driver_id)
                car.save_to_db(fs.mycursor)
                fs.mydb.commit()

                # Accident info
                report_num = int(request.form.get("accident_report_number"))
                location = request.form.get("accident_location")
                date = request.form.get("accident_date")
                accident = Accident(report_num, location, date)
                accident.save_to_db(fs.mycursor)
                fs.mydb.commit()

                # Link car to accident
                car.link_to_accident(fs.mycursor, accident.report_number)

                fs.mydb.commit()

                message = f"Person {person.name}, Car {car.model}, and Accident {accident.report_number} saved and linked!"

            except Exception as e:
                fs.mydb.rollback()
                message = f"Something went wrong: {str(e)}"
        elif "remove_report" in request.form:

            driver_id = int(request.form.get("remove_driver_id"))

            Person.remove_record(fs.mycursor, driver_id)

            fs.mydb.commit()

            message = f"Record featuring driver ID: {driver_id} removed from the database"

            #use method that removes record based on driver_id
        elif "drop_database" in request.form:

            fs.clear_all_tables()  # Drops the database

            message = "Removed all records"
        

    # ✅ This is outside the POST block, so it runs for both GET and POST
    fs.mycursor.execute("SELECT * FROM customers")
    people = fs.mycursor.fetchall()

    fs.mycursor.execute("SELECT * FROM cars")
    cars = fs.mycursor.fetchall()

    fs.mycursor.execute("SELECT * FROM accidents")
    accidents = fs.mycursor.fetchall()

    fs.mycursor.execute("""
        SELECT 
            customers.driver_id, customers.name, customers.address,
            cars.license, cars.model, cars.year,
            accidents.report_number, accidents.location, accidents.date
        FROM customers
        LEFT JOIN cars ON customers.driver_id = cars.driver_id
        LEFT JOIN car_accidents ON cars.license = car_accidents.license
        LEFT JOIN accidents ON car_accidents.report_number = accidents.report_number
        ORDER BY customers.name ASC, accidents.date DESC
    """)
    full_records = fs.mycursor.fetchall()

    return render_template("index.html", message=message, people=people, cars=cars, accidents=accidents, full_records=full_records)

    # fs.drop_database()  # Drops the database

if __name__ == '__main__':
    app.run(debug=True)
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

    return render_template("index.html", message=message)


    # colton = Person(21, "Colton", "422 montroyal Blvd.")
    # colton.save_to_db(fs.mycursor)

    # camero = Car(11111, "Camero", 2025, 21)
    # camero.save_to_db(fs.mycursor)

    # head_on_collision = Accident(212, "Edgemont Village", '2010-08-11')
    # head_on_collision.save_to_db(fs.mycursor)

    # # Commit all inserts before linking
    # fs.mydb.commit()

    # # Automatically link the car and accident
    # camero.link_to_accident(fs.mycursor, 212)
    # fs.mydb.commit()
    # print("Car-Accident relationship recorded.")

    # print("Person saved:", colton)
    # print("Car saved:", camero)
    # print("Accident reported:", head_on_collision)


    # fs.drop_database()  # Drops the database

if __name__ == '__main__':
    app.run(debug=True)
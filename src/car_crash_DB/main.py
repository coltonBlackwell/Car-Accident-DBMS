from entities import Person, FileSystem, Car, Accident 

def main():

    fs = FileSystem()
    fs.create_person_table()
    fs.create_cars_table()
    fs.create_accidents_table()
    fs.create_car_accidents_table()

    colton = Person(21, "Colton", "422 montroyal Blvd.")
    colton.save_to_db(fs.mycursor)

    camero = Car(11111, "Camero", 2025, 21)
    camero.save_to_db(fs.mycursor)

    head_on_collision = Accident(212, "Edgemont Village", '2010-08-11')
    head_on_collision.save_to_db(fs.mycursor)

    # Commit all inserts before linking
    fs.mydb.commit()

    # Automatically link the car and accident
    camero.link_to_accident(fs.mycursor, 212)
    fs.mydb.commit()
    print("Car-Accident relationship recorded.")

    print("Person saved:", colton)
    print("Car saved:", camero)
    print("Accident reported:", head_on_collision)


    # fs.drop_database()  # Drops the database

if __name__ == '__main__':
    main()
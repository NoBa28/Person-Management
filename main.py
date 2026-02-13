from controller.PersonController import PersonController
from model.PersonModel import PersonModel
from view.PersonView import PersonView
from db import setup_db

if __name__ == "__main__":
    setup_db.create_address_table()
    setup_db.create_person_table()
    person_view = PersonView()
    person_model = PersonModel()
    person_controller = PersonController(person_model, person_view)
    person_controller.run()

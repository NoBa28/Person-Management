from view.PersonView import PersonView
from model.PersonModel import PersonModel
from controller.PersonController import PersonController

if __name__ == "__main__":
    person_view = PersonView()
    person_model = PersonModel()
    person_controller = PersonController(person_model, person_view)
    person_controller.run()

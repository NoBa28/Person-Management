from controller.PersonController import PersonController
from model.PersonModel import PersonModel
from view.PersonView import PersonView

if __name__ == "__main__":
    person_view = PersonView()
    person_model = PersonModel()
    person_controller = PersonController(person_model, person_view)
    person_controller.run()

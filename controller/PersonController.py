from datetime import datetime

from common.InputValidator import InputValidator
from common.Operation import Operation
from model.Address import Address
from model.PersonModel import Person, PersonModel
from view.PersonView import PersonView


class PersonController:

    def __init__(self, model: PersonModel, view: PersonView):
        self.view = view
        self.model = model

    def create_address(self) -> Address:
        street = self.view.ask("Strasse", InputValidator.is_string)
        house_num = self.view.ask("Hausnummer", InputValidator.is_number)
        zip_code = self.view.ask("Postleitzahl", InputValidator.is_zip_code,
                                 "Ungueltige Postleitzahl: Min 4, Max. 5 Zahlen")
        city = self.view.ask("Stadt", InputValidator.is_string)
        country = self.view.ask("Land", InputValidator.is_string)
        return Address(street, int(house_num), zip_code, city, country)

    def create_person(self) -> Person:
        first_name = self.view.ask("Vorname", InputValidator.is_string)
        last_name = self.view.ask("Nachname", InputValidator.is_string)
        birth_date_str = self.view.ask("Geburtsdatum (DD.MM.YYYY)", InputValidator.is_date, "Ungueltiges Format")
        birth_date = datetime.strptime(birth_date_str, "%d.%m.%Y").date()
        email = self.view.ask("E-Mail", InputValidator.is_email, "Ungueltige E-Mail")
        person = Person(first_name, last_name, birth_date, email, self.create_address())
        self.model.insert_person(person)
        return person

    def get_person(self) -> Person:
        persons = self.model.get_all_persons()
        person_dict = {p.person_id: p for p in persons}
        while True:
            pers_id = self.view.ask_person_to_update(
                "Geben sie die ID der Person ein, welche Sie bearbeiten moechten.")
            person = person_dict.get(pers_id)
            if person:
                return person
            else:
                self.view.print_invalid_person_msg()

    def update_person(self):
        person_to_update = self.get_person()
        self.view.print_person(person_to_update)
        update_person = self.view.collect_person_update(person_to_update)
        self.model.update_person(person_to_update, update_person)

    def delete_person(self):
        person_to_delete = self.get_person()
        self.view.print_person(person_to_delete)
        self.model.delete_person(person_to_delete)

    def handle_operation(self, operation: str):
        match operation:
            case Operation.CREATE.value:
                self.create_person()
            case Operation.UPDATE.value:
                self.update_person()
                pass
            case Operation.DELETE.value:
                self.delete_person()
                pass
            case Operation.PRINT.value:
                self.view.print_persons(self.model.get_all_persons())

    def run(self):
        self.view.print_header()

        while True:
            if not self.model.get_all_persons():
                self.view.print_program_start()
                if not self.view.ask_yes_no("Moechten Sie eine Person erfassen?"):
                    self.view.print_program_end()
                    return
            self.view.print_option_menu()
            operation = self.view.ask("Auswahl", InputValidator.is_number)
            self.handle_operation(operation)

            if self.view.ask_yes_no("Programm beenden?"):
                self.view.print_program_end()
                return

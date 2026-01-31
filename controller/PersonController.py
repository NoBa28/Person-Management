import re
from datetime import datetime

from model.Address import Address
from model.PersonModel import Person, PersonModel
from view.PersonView import PersonView


def is_valid_string(user_in: str) -> bool:
    return bool(re.fullmatch("[a-zA-Z]+", user_in))


def is_valid_date(user_in: str) -> bool:
    try:
        datetime.strptime(user_in, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def is_valid_email(user_in: str) -> bool:
    return bool(re.fullmatch("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", user_in))


def is_valid_number(user_in: str) -> bool:
    return bool(re.fullmatch("[0-9]+", user_in))


def is_valid_zip_code(user_in: str) -> bool:
    return bool(re.fullmatch("[0-9]{4,5}+", user_in))


def is_valid_yes_no_string(user_in: str) -> bool:
    return bool(re.fullmatch("[yYnN]+", user_in))


class PersonController:

    def __init__(self, person_model: PersonModel, view: PersonView):
        self.view = view
        self.person_model = person_model

    def create_address(self) -> Address:
        street = self.view.start_query("Strasse", is_valid_string)
        house_num = self.view.start_query("Hausnummer", is_valid_number)
        zip_code = self.view.start_query("Postleitzahl", is_valid_zip_code,
                                         "Ungueltige Postleitzahl: Min 4, Max. 5 Zahlen")
        city = self.view.start_query("Stadt", is_valid_string)
        country = self.view.start_query("Land", is_valid_string)
        return Address(street, house_num, zip_code, city, country)

    def create_person(self) -> Person:
        first_name = self.view.start_query("Vorname", is_valid_string)
        last_name = self.view.start_query("Nachname", is_valid_string)
        birth_date = self.view.start_query("Geburtsdatum", is_valid_date, "Ungueltiges Datum, Format: dd.MM.yyyy")
        email = self.view.start_query("E-Mail", is_valid_email, "Ungueltige E-Mail")
        person = Person(first_name, last_name, birth_date, email, self.create_address())
        self.add_person(person)
        return person

    def add_person(self, person: Person):
        self.person_model.add_person(person)

    def print_person(self):
        self.view.print_persons(self.person_model.get_persons_in_record())

    def update_person(self, person: Person):
        self.person_model.update_person(person)

    def delete_person(self, person: Person):
        self.person_model.delete_person(person)

    def get_persons_in_record(self) -> list[Person]:
        return self.person_model.get_persons_in_record()

    def start_operation(self):
        operation = self.view.start_query("Was moechten Sie tun? ", is_valid_number)
        match operation:
            case "1":
                self.create_person()
            case "2":
                self.update_person()
                pass
            case "3":
                self.delete_person()
                pass
            case "4":
                self.print_person()

    def start(self):
        self.view.print_header()
        input_value = ""
        while input_value == "" or input_value == "n":
            if not self.get_persons_in_record():
                self.view.print_program_start()
                input_value = self.view.start_query("Y/N: ", is_valid_yes_no_string).lower()
                if input_value.lower() == "y":
                    self.view.print_options()
                    self.start_operation()
                    self.view.print_program_end_query()
                    input_value = self.view.start_query("Y/N: ", is_valid_yes_no_string).lower()
                else:
                    self.view.print_program_end()
                    return
            else:
                self.view.print_options()
                self.start_operation()
                self.view.print_program_end_query()
                input_value = self.view.start_query("Y/N: ", is_valid_yes_no_string).lower()

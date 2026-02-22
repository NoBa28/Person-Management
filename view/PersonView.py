from datetime import datetime
from typing import TypeVar, Callable, Optional

from common.InputValidator import InputValidator
from dto.AddressUpdate import AddressUpdate
from dto.PersonUpdate import PersonUpdate
from model.Address import Address
from model.Person import Person

T = TypeVar("T")


class PersonView:
    DEFAULT_ERROR = "Ungueltige Eingabe"

    @staticmethod
    def ask(
            label: str,
            validator: Callable[[str], bool],
            converter: Callable[[str], T] = str,
            error_msg=DEFAULT_ERROR
    ) -> T:
        while True:
            input_value = input(f"{label}: ")
            if validator(input_value):
                return converter(input_value)
            else:
                print(error_msg)

    def ask_yes_no(self, label: str) -> bool:
        input_value = self.ask(label + "(J/N)", InputValidator.is_yes_no)
        return input_value.lower() == "j"

    def ask_person_to_update(self, prompt: str) -> int:
        return self.ask(prompt, InputValidator.is_number, int)

    def ask_optional(
            self,
            label: str,
            current_value: T,
            validator: Callable[[str], bool],
            converter: Callable[[str], T] = str,
    ) -> Optional[T]:
        prompt = f"{label} (Aktuell: {current_value}, Enter = keine Änderung): "
        while True:
            value = input(prompt).strip()
            if value == "":
                return None
            if validator(value):
                return converter(value)
            print(self.DEFAULT_ERROR)

    @staticmethod
    def print_header():
        print("Personenverwaltung\n")

    @staticmethod
    def print_program_start():
        print("--------------------")
        print("Es wurden noch keine Personen erfast.")

    @staticmethod
    def print_option_menu():
        print("--------------------")
        print("Was möchten Sie tun?")
        print("1 - Person hinzufuegen")
        print("2 - Person bearbeiten")
        print("3 - Person loeschen")
        print("4 - Erfasste Personen ausgeben")
        print("--------------------")

    @staticmethod
    def print_program_end():
        print("Programm wird beendet")

    @staticmethod
    def print_invalid_person_msg():
        print("Eine Person mit dieser ID existiert nicht.")

    @staticmethod
    def print_update_menu():
        print("--------------------")
        print("Was moechten sie aendern?")
        print("1 - Vorname")
        print("2 - Nachname")
        print("3 - Geburtsdatum")
        print("4 - E-Mail")
        print("5 - Adresse")
        print("--------------------")

    def collect_address_update(self, address: Address) -> AddressUpdate:
        update = AddressUpdate()

        update.street = self.ask_optional("Strasse", address.street, InputValidator.is_string)
        update.house_num = self.ask_optional("Hausnummer", address.house_num, InputValidator.is_number, int)
        update.zip_code = self.ask_optional("Postleitzahl", address.zip_code, InputValidator.is_zip_code)
        update.city = self.ask_optional("Stadt", address.city, InputValidator.is_string)
        update.country = self.ask_optional("Land", address.country, InputValidator.is_string)
        return update

    def collect_person_update(self, person: Person) -> PersonUpdate:
        update = PersonUpdate()

        self.print_update_menu()
        choice = int(self.ask("Auswahl", InputValidator.is_number))

        match choice:
            case 1:
                update.first_name = self.ask("Neuer Vorname", InputValidator.is_string)
            case 2:
                update.last_name = self.ask("Neuer Nachname", InputValidator.is_string)
            case 3:
                update.birth_date = self.ask(
                    "Neues Geburtsdatum",
                    InputValidator.is_date,
                    lambda x: datetime.strptime(x, "%d.%m.%Y").date()
                )
            case 4:
                update.mail = self.ask("Neue E-Mail", InputValidator.is_email)
            case 5:
                update.address = self.collect_address_update(person.address)
            case _:
                print(self.DEFAULT_ERROR)

        return update

    @staticmethod
    def print_person(person: Person):
        print()
        print(person)

    @staticmethod
    def print_persons(persons: list[Person]):
        for person in persons:
            print(person)

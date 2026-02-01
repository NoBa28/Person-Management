from common.InputValidator import InputValidator
from dto.AddressUpdate import AddressUpdate
from dto.PersonUpdate import PersonUpdate
from model.Address import Address
from model.Person import Person


class PersonView:
    DEFAULT_ERROR = "Ungueltige Eingabe"

    def ask(self, label: str, validator, error_msg=DEFAULT_ERROR) -> str:
        while True:
            input_value = input(f"{label}: ")
            if validator(input_value):
                return input_value
            else:
                print(error_msg)

    def ask_yes_no(self, label: str) -> bool:
        input_value = self.ask(label + "(Y/N)", InputValidator.is_yes_no)
        return input_value.lower() == "y"

    def print_header(self):
        print("Personenverwaltung\n")

    def print_program_start(self):
        print("--------------------")
        print("Es wurden noch keine Personen erfast.")

    def print_option_menu(self):
        print("--------------------")
        print("Was möchten Sie tun?")
        print("1 - Person hinzufuegen")
        print("2 - Person bearbeiten")
        print("3 - Person loeschen")
        print("4 - Erfasste Personen ausgeben")
        print("--------------------")

    def print_program_end(self):
        print("Programm wird beendet")

    def ask_person_to_update(self, prompt: str) -> int:
        return int(self.ask(prompt, InputValidator.is_number))

    def print_invalid_person_msg(self):
        print("Eine Person mit dieser Nummer existiert nicht.")

    def print_update_menu(self):
        print("--------------------")
        print("Was moechten sie aendern?")
        print("1 - Vorname")
        print("2 - Nachname")
        print("3 - Geburtsdatum")
        print("4 - E-Mail")
        print("5 - Adresse")
        print("--------------------")

    def ask_optional(self, label: str, current_value: str, validator) -> str:
        prompt = f"{label} (aktuell: {current_value}, Enter = keine Änderung): "
        while True:
            value = input(prompt).strip()
            if value == "":
                return current_value
            if validator(value):
                return value
            print(self.DEFAULT_ERROR)

    def collect_address_update(self, address: Address) -> AddressUpdate:
        update = AddressUpdate()

        update.street = self.ask_optional("Strasse", address.street, InputValidator.is_string)
        update.house_num = self.ask_optional("Hausnummer", address.house_num, InputValidator.is_number)
        update.zip_code = self.ask_optional("Postleitzahl", address.zip_code, InputValidator.is_zip_code)
        update.city = self.ask_optional("Stadt", address.city, InputValidator.is_string)
        update.country = self.ask_optional("Land", address.country, InputValidator.is_string)
        return update

    def collect_person_update(self, person: Person) -> PersonUpdate:
        update = PersonUpdate()

        while True:
            self.print_update_menu()
            print("0 - Fertig / Beenden")
            choice = self.ask("Auswahl", InputValidator.is_number)

            match choice:
                case "0":
                    break
                case "1":
                    update.first_name = self.ask("Neuer Vorname", InputValidator.is_string)
                case "2":
                    update.last_name = self.ask("Neuer Nachname", InputValidator.is_string)
                case "3":
                    update.birth_date = self.ask("Neues Geburtsdatum", InputValidator.is_date)
                case "4":
                    update.mail = self.ask("Neue E-Mail", InputValidator.is_email)
                case "5":
                    update.address = self.collect_address_update(person.address)
                case _:
                    print(self.DEFAULT_ERROR)
        return update

    def print_person(self, person: Person):
        print(person)

    def print_persons(self, persons: list[Person]):
        for number, person in enumerate(persons, start=1):
            print(f"\nPerson: {number}")
            print(person)

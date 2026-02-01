from common.InputValidator import InputValidator
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

    def ask_yes_no(self, label:str) -> bool:
        value = self.ask(label + "(Y/N)", InputValidator.is_yes_no)
        return value.lower() == "y"

    def print_header(self):
        print("Personenverwaltung\n")

    def print_program_start(self):
        print("Es wurden noch keine Personen erfast.")

    def print_options(self):
        print("--------------------")
        print("Was möchten Sie tun?")
        print("1 - Person hinzufuegen")
        print("2 - Person bearbeiten")
        print("3 - Person loeschen")
        print("4 - Erfasste Personen ausgeben")
        print("--------------------")

    def print_program_end(self):
        print("Programm wird beendet")

    def ask_which_person_to_update(self):
        print("Welche Person moechten Sie updaten?")

    def print_persons(self, persons: list[Person]):
        for person in persons:
            print(person)

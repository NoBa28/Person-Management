from model.Person import Person


class PersonView:
    _default_error_msg = "Ungueltige Eingabe"

    def start_query(self, label: str, validator, error_msg=_default_error_msg) -> str:
        while True:
            input_value = input(f"{label}: ")
            if validator(input_value):
                return input_value
            else:
                print(error_msg)

    def get_operation_from_input(self, validator, error_msg=_default_error_msg) -> str:
        input_value = self.start_query(validator, error_msg)
        return input_value

    def print_header(self):
        print("Personenverwaltung\n")

    def print_program_start(self):
        print("Es wurden noch keine Personen erfast.")
        print("Moechten Sie eine Person erfassen?")

    def print_options(self):
        print("--------------------")
        print("Was möchten Sie tun?")
        print("1 - Person hinzufuegen")
        print("2 - Person bearbeiten")
        print("3 - Person loeschen")
        print("4 - Erfasste Personen ausgeben")
        print("--------------------")

    def print_program_end_query(self):
        print("Moechten Sie das Programm Beenden?")

    def print_program_end(self):
        print("Programm wird beendet")

    def print_persons(self, persons: list[Person]):
        for person in persons:
            print(person)

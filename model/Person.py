from datetime import date

from model.Address import Address


class Person:

    def __init__(self,
                 first_name: str,
                 last_name: str,
                 birth_date: date,
                 mail: str,
                 address: Address,
                 person_id: int = None):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.mail = mail
        self.address = address

    def __str__(self):
        return (f"Person ID: {self.person_id}\n"
                f"Vorname: {self.first_name}\n"
                f"Nachname: {self.last_name}\n"
                f"Geburtsdatum: {self.birth_date.strftime("%d.%m.%Y")}\n"
                f"E-Mail: {self.mail}\n"
                f"{self.address}")

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return (self.person_id == other.person_id and
                self.first_name == other.first_name and
                self.last_name == other.last_name and
                self.birth_date == other.birth_date and
                self.mail == other.mail and
                self.address == other.address)

    def __hash__(self):
        return hash((self.person_id,
                     self.first_name,
                     self.last_name,
                     self.birth_date,
                     self.mail,
                     self.address))

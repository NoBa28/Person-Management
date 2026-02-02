from __future__ import annotations

from dto.AddressUpdate import AddressUpdate
from dto.PersonUpdate import PersonUpdate
from model.Address import Address
from model.Person import Person


class PersonModel:
    PERSON_FIELDS = ("first_name", "last_name", "birth_date", "mail")
    ADDRESS_FIELDS = ("street", "house_num", "zip_code", "city", "country")

    def __init__(self):
        self._all_persons: list[Person] = []

    def find_person_in_record(self, person: Person) -> Person | None:
        return next(
            (p for p in self._all_persons
             if p == person),
            None
        )

    @staticmethod
    def apply_update(target, update, fields: tuple[str, ...]):
        for attr in fields:
            value = getattr(update, attr)
            if value is not None:
                setattr(target, attr, value)

    def add_person(self, person: Person):
        self._all_persons.append(person)

    def update_address(self, address: Address, update_address: AddressUpdate):
        self.apply_update(address, update_address, self.ADDRESS_FIELDS)

    def update_person(self, person: Person, update_person: PersonUpdate):
        self.apply_update(person, update_person, self.PERSON_FIELDS)
        if update_person.address is not None:
            self.update_address(person.address, update_person.address)

    def delete_person(self, person: Person):
        self._all_persons.remove(person)

    def get_all_persons(self):
        return self._all_persons

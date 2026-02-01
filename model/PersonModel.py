from __future__ import annotations

from dataclasses import is_dataclass, fields
from typing import Any

from dto.AddressUpdate import AddressUpdate
from dto.PersonUpdate import PersonUpdate
from model.Address import Address
from model.Person import Person


def apply_patch(target: Any, patch: Any) -> None:
    if not is_dataclass(patch):
        raise TypeError(f"Patch muss eine Dataclass sein, ist {type(patch)}")
    for f in fields(type(patch)):
        value = getattr(patch, f.name)
        if value is not None:
            setattr(target, f.name, value)


class PersonModel:

    def __init__(self):
        self._all_persons: list[Person] = []

    def find_person_in_record(self, person: Person) -> Person | None:
        return next(
            (p for p in self._all_persons
             if p == person),
            None
        )

    def add_person(self, person: Person):
        self._all_persons.append(person)

    def update_address(self, address: Address, update_address: AddressUpdate):
        if update_address is None:
            return
        apply_patch(address, update_address)

    def update_person(self, person: Person, update_person: PersonUpdate):
        apply_patch(person, update_person)
        if update_person.address:
            self.update_address(person.address, update_person.address)
            update_person.address = None

    def delete_person(self, person: Person):
        self._all_persons.remove(person)

    def get_all_persons(self):
        return self._all_persons

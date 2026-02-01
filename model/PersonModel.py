from model.Person import Person


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

    def update_person(self, person: Person):
        person_to_update = self.find_person_in_record(person)

    def delete_person(self, person: Person):
        self._all_persons.remove(person)

    def get_all_persons(self):
        return self._all_persons

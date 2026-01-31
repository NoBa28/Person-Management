from model.Person import Person

class PersonModel:

    _persons_in_record = []

    def __init__(self):
        pass

    def find_person_in_record(self, person:Person) -> Person | None:
        return next(
            (p for p in self._persons_in_record
             if p == person),
            None
        )

    def add_person(self, person: Person):
        self._persons_in_record.append(person)

    def update_person(self, person: Person):
        person_to_update = self.find_person_in_record(person)

    def delete_person(self, person: Person):
        self._persons_in_record.remove(person)

    def get_persons_in_record(self):
        return self._persons_in_record

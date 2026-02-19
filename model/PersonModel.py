from __future__ import annotations

import mysql.connector

from db.db_config import DB_CONFIG
from dto.AddressUpdate import AddressUpdate
from dto.PersonUpdate import PersonUpdate
from model.Address import Address
from model.Person import Person


class PersonModel:
    PERSON_FIELDS = ("first_name", "last_name", "birth_date", "mail")
    ADDRESS_FIELDS = ("street", "house_num", "zip_code", "city", "country")

    @staticmethod
    def apply_update(target, update, fields: tuple[str, ...]):
        for attr in fields:
            value = getattr(update, attr)
            if value is not None:
                setattr(target, attr, value)

    @staticmethod
    def get_address_id(cursor, address):
        cursor.execute("""
                       SELECT id
                       FROM address
                       WHERE street = %s
                         AND house_num = %s
                         AND zip_code = %s
                         AND city = %s
                         AND country = %s
                       """,
                       (address.street,
                        address.house_num,
                        address.zip_code,
                        address.city,
                        address.country)
                       )
        result = cursor.fetchone()

        if result:
            return result[0]
        return None

    def insert_person(self, person: Person):
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                existing_address_id = self.get_address_id(cursor, person.address)
                if existing_address_id:
                    person.address.address_id = existing_address_id
                else:
                    cursor.execute(
                        "INSERT INTO address (street, house_num, zip_code, city, country) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (person.address.street,
                         person.address.house_num,
                         person.address.zip_code,
                         person.address.city,
                         person.address.country)
                    )
                    person.address.address_id = cursor.lastrowid

                cursor.execute(
                    "INSERT INTO person (first_name, last_name, birth_date, mail, address_id) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (person.first_name,
                     person.last_name,
                     person.birth_date,
                     person.mail,
                     person.address.address_id)
                )
                conn.commit()

    def update_address(self, address: Address, update_address: AddressUpdate):
        self.apply_update(address, update_address, self.ADDRESS_FIELDS)

    def update_person(self, person: Person, update_person: PersonUpdate):
        self.apply_update(person, update_person, self.PERSON_FIELDS)
        self.update_in_db("person", update_person, person.person_id, self.PERSON_FIELDS)
        if update_person.address is not None:
            self.update_address(person.address, update_person.address)
            self.update_in_db("address", update_person.address, person.address.address_id, self.ADDRESS_FIELDS)

    @staticmethod
    def update_in_db(table_name: str, dto, obj_id: int, fields: tuple[str, ...]):
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                set_queries = []
                values = []

                for attr in fields:
                    value = getattr(dto, attr)
                    if value is not None:
                        set_queries.append(f"{attr} = %s")
                        values.append(value)
                if not set_queries:
                    return
                values.append(obj_id)
                cursor.execute(
                    f"UPDATE {table_name} SET {', '.join(set_queries)} WHERE id = %s",
                    values
                )
                conn.commit()

    @staticmethod
    def delete_person(person: Person):
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT address_id FROM person WHERE id = %s", (person.person_id,))
                result = cursor.fetchone()
                if not result:
                    return
                address_id = result[0]
                cursor.execute("DELETE FROM person WHERE id = %s", (person.person_id,))
                cursor.execute("SELECT COUNT(*) FROM person WHERE address_id = %s", (address_id,))
                count = cursor.fetchone()[0]
                if count == 0:
                    cursor.execute( "DELETE FROM address WHERE id = %s", (address_id,))
                conn.commit()

    @staticmethod
    def get_all_persons() -> list[Person]:
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""
                               SELECT p.id         AS person_id,
                                      p.first_name,
                                      p.last_name,
                                      p.birth_date,
                                      p.mail,
                                      a.address_id AS address_id,
                                      a.street,
                                      a.house_num,
                                      a.zip_code,
                                      a.city,
                                      a.country
                               FROM person p
                                        JOIN address a ON p.address_id = a.id
                               """)
                return [
                    Person(
                        person_id=row['person_id'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        birth_date=row['birth_date'],
                        mail=row['mail'],
                        address=Address(
                            address_id=row['address_id'],
                            street=row['street'],
                            house_num=row['house_num'],
                            zip_code=row['zip_code'],
                            city=row['city'],
                            country=row['country']
                        )
                    )
                    for row in cursor.fetchall()
                ]

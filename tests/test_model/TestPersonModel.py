import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from dto.AddressUpdate import AddressUpdate
from dto.PersonUpdate import PersonUpdate
from model.Address import Address
from model.Person import Person
from model.PersonModel import PersonModel


class TestPersonModel(unittest.TestCase):

    def setUp(self):
        self.model = PersonModel()
        self.address = Address("Musterstrasse",
                               12,
                               "1111",
                               "Musterhausen",
                               "Musterland",
                               address_id=1)
        self.person = Person("Max",
                             "Mustermann",
                             date(2000, 1, 1),
                             "max@testmail.com",
                             self.address,
                             person_id=1)

    def test_apply_update_updates_attributes(self):
        update = PersonUpdate(
            first_name="John",
            last_name=None,
            birth_date=None,
            mail="john.doe@test.com"
        )
        PersonModel.apply_update(self.person, update, PersonModel.PERSON_FIELDS)

        self.assertEqual(self.person.first_name, "John")
        self.assertEqual(self.person.last_name, "Mustermann")
        self.assertEqual(self.person.birth_date, date(2000, 1, 1))
        self.assertEqual(self.person.mail, "john.doe@test.com")

    @patch("model.PersonModel.DB.connect")
    def test_get_address_id_exists_and_not_exists(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.return_value = [42]
        address_id = PersonModel.get_address_id(mock_cursor, self.address)
        self.assertEqual(address_id, 42)

        mock_cursor.fetchone.return_value = None
        address_id = PersonModel.get_address_id(mock_cursor, self.address)
        self.assertIsNone(address_id)

    @patch("model.PersonModel.DB.connect")
    def test_isnert_person_new_and_existing_address(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.return_value = [100]
        address = Address("Schneeweg",
                          1,
                          "1234",
                          "Schnellstadt",
                          "Land")
        person = Person("Alice",
                        "Test",
                        date(1990, 10, 1),
                        "a@test.com",
                        address)
        self.model.insert_person(person)

        self.assertEqual(person.address.address_id, 100)
        mock_cursor.execute.assert_any_call(
            "INSERT INTO person (first_name, last_name, birth_date, mail, address_id) "
            "VALUES (%s, %s, %s, %s, %s)",
            (person.first_name, person.last_name, person.birth_date, person.mail, 100)
        )

        mock_cursor.fetchone.return_value = None
        mock_cursor.lastrowid = 200
        address2 = Address("Neustrasse",
                           15,
                           "5678",
                           "Neuhausen",
                           "Kalinka")
        person2 = Person("Bob",
                         "Test",
                         date(1999, 11, 21),
                         "bob@mailo.com",
                         address2)
        self.model.insert_person(person2)

        self.assertEqual(person2.address.address_id, 200)
        mock_conn.commit.assert_called()

    def test_update_address(self):
        update = AddressUpdate(street="Gehweg", city=None)
        self.model.update_address(self.address, update)
        self.assertEqual(self.address.street, "Gehweg")
        self.assertEqual(self.address.city, "Musterhausen")

    @patch("model.PersonModel.PersonModel.update_in_db")
    def test_update_person_with_and_without_address(self, mock_update_in_db):
        update_person = PersonUpdate(first_name="Jane", address=None)
        self.model.update_person(self.person, update_person)
        self.assertEqual(self.person.first_name, "Jane")
        mock_update_in_db.assert_called_with("person", update_person, self.person.person_id, PersonModel.PERSON_FIELDS)

        update_person.address = AddressUpdate(street="Neustrasse")
        self.model.update_person(self.person, update_person)
        self.assertEqual(self.person.address.street, "Neustrasse")
        self.assertEqual(mock_update_in_db.call_count, 3)

    @patch("model.PersonModel.DB.connect")
    def test_update_in_db_with_and_without_changes(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        dto = PersonUpdate()
        PersonModel.update_in_db("person", dto, 1, PersonModel.PERSON_FIELDS)
        mock_cursor.execute.assert_not_called()

        dto2 = PersonUpdate(first_name="X")
        PersonModel.update_in_db("person", dto2, 1, PersonModel.PERSON_FIELDS)
        mock_cursor.execute.assert_called_once()

    @patch("model.PersonModel.DB.connect")
    def test_delete_person_variants(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # --- variant 1: adress is used by other persons (no DELETE address) ---
        # fetchone for SELECT address_id, SELECT COUNT(*)
        mock_cursor.fetchone.side_effect = [[50], [2]]  # COUNT(*) > 0
        PersonModel.delete_person(self.person)
        # DELETE person needs to be called
        calls_sql = [call.args[0] for call in mock_cursor.execute.call_args_list]
        self.assertIn("DELETE FROM person WHERE id = %s", calls_sql)
        # DELETE address not allowed
        self.assertNotIn("DELETE FROM address WHERE id = %s", calls_sql)
        mock_conn.commit.assert_called()

        mock_cursor.reset_mock()
        mock_conn.reset_mock()

        # --- variant 2: adress has no usages (DELETE address) ---
        mock_cursor.fetchone.side_effect = [[50], [0]]  # COUNT(*) = 0
        PersonModel.delete_person(self.person)
        calls_sql = [call.args[0] for call in mock_cursor.execute.call_args_list]
        self.assertIn("DELETE FROM person WHERE id = %s", calls_sql)
        self.assertIn("DELETE FROM address WHERE id = %s", calls_sql)
        mock_conn.commit.assert_called()

        mock_cursor.reset_mock()
        mock_conn.reset_mock()

        # --- variant 3: person doesn't exist (no deletion) ---
        mock_cursor.fetchone.side_effect = [None]
        PersonModel.delete_person(self.person)
        # execute may only have been called once (SELECT address_id)
        mock_cursor.execute.assert_called_once_with(
            "SELECT address_id FROM person WHERE id = %s", (self.person.person_id,)
        )

    @patch("model.PersonModel.DB.connect")
    def test_get_all_persons(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            {
                'person_id': 1,
                'first_name': 'Max',
                'last_name': 'Mustermann',
                'birth_date': date(2000, 1, 1),
                'mail': 'max@mail.com',
                'address_id': 1,
                'street': 'Street',
                'house_num': 10,
                'zip_code': '12345',
                'city': 'City',
                'country': 'Country'
            }
        ]
        persons = PersonModel.get_all_persons()
        self.assertEqual(len(persons), 1)
        self.assertEqual(persons[0].first_name, "Max")
        self.assertIsInstance(persons[0].address, Address)

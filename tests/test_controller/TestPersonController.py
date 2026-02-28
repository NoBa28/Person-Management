import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from common.Operation import Operation
from controller.PersonController import PersonController
from model.Address import Address
from model.Person import Person


class TestPersonController(unittest.TestCase):

    def setUp(self):
        self.mock_model = MagicMock()
        self.mock_view = MagicMock()
        self.controller = PersonController(self.mock_model, self.mock_view)

    # noinspection PyTypeChecker
    @staticmethod
    def create_dummy_person() -> Person:
        return Person("Max",
                      "Mustermann",
                      date(2000, 1, 1),
                      "max@testmail.com",
                      None)

    def test_create_address(self):
        self.mock_view.ask.side_effect = [
            "Musterstrasse",
            "12",
            "1111",
            "Musterhausen",
            "Musterland"
        ]
        address = self.controller.create_address()

        self.assertIsInstance(address, Address)
        self.assertEqual(address.street, "Musterstrasse")
        self.assertEqual(address.house_num, 12)
        self.assertEqual(address.zip_code, "1111")
        self.assertEqual(address.city, "Musterhausen")
        self.assertEqual(address.country, "Musterland")

    @patch("controller.PersonController.PersonController.create_address")
    def test_create_person(self, mock_create_address):
        mock_create_address.return_value = Address(street="Musterstrasse",
                                                   house_num=12,
                                                   zip_code="1111",
                                                   city="Musterhausen",
                                                   country="Musterland")
        self.mock_view.ask.side_effect = [
            "Max",
            "Mustermann",
            date(2000, 1, 1),
            "max@testmail.com"
        ]
        person = self.controller.create_person()

        self.mock_model.insert_person.assert_called_once()
        self.assertEqual(person.first_name, "Max")
        self.assertEqual(person.last_name, "Mustermann")
        self.assertEqual(person.birth_date, date(2000, 1, 1))
        self.assertEqual(person.mail, "max@testmail.com")

    def test_get_person_valid(self):
        person = self.create_dummy_person()
        person.person_id = 1

        self.mock_model.get_all_persons.return_value = [person]
        self.mock_view.ask_person_to_update.return_value = 1

        result = self.controller.get_person()

        self.assertEqual(result, person)

    def test_get_person_invalid_then_valid(self):
        person = self.create_dummy_person()
        person.person_id = 1

        self.mock_model.get_all_persons.return_value = [person]
        self.mock_view.ask_person_to_update.side_effect = [999, 1]

        result = self.controller.get_person()

        self.assertEqual(result, person)
        self.assertTrue(self.mock_view.print_invalid_person_msg.called)

    def test_update_person(self):
        person = self.create_dummy_person()
        person.person_id = 1

        self.controller.get_person = MagicMock(return_value=person)
        self.mock_view.collect_person_update.return_value = "UPDATE_DTO"
        self.controller.update_person()
        self.mock_model.update_person.assert_called_once_with(person, "UPDATE_DTO")

    def test_delete_person(self):
        person = self.create_dummy_person()

        self.controller.get_person = MagicMock(return_value=person)
        self.controller.delete_person()
        self.mock_model.delete_person.assert_called_once_with(person)

    def test_handle_operation_create(self):
        self.controller.create_person = MagicMock()
        self.controller.handle_operation(Operation.CREATE.value)
        self.controller.create_person.assert_called_once()

    def test_handle_operation_update(self):
        self.controller.update_person = MagicMock()
        self.controller.handle_operation(Operation.UPDATE.value)
        self.controller.update_person.assert_called_once()

    def test_handle_operation_delete(self):
        self.controller.delete_person = MagicMock()
        self.controller.handle_operation(Operation.DELETE.value)
        self.controller.delete_person.assert_called_once()

    def test_handle_operation_print(self):
        self.mock_model.get_all_person.return_value = []
        self.controller.handle_operation(Operation.PRINT.value)
        self.mock_view.print_persons.assert_called_once()

    def test_run_exit_immediatly(self):
        self.mock_model.get_all_persons.return_value = []
        self.mock_view.ask_yes_no.return_value = False

        self.controller.run()

        self.mock_view.print_program_end.assert_called_once()

    def test_run_single_iteration_then_exit(self):
        self.mock_model.get_all_persons.side_effect = [
            [],
            [1],
            [1]
        ]
        self.mock_view.ask_yes_no.side_effect = [
            True,  # create first person?
            True  # exit program?
        ]
        self.mock_view.ask.return_value = Operation.PRINT.value

        self.controller.handle_operation = MagicMock()
        self.controller.run()

        self.controller.handle_operation.assert_called_once()
        self.mock_view.print_program_end.assert_called_once()

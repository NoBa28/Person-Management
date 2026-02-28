import unittest
from common.InputValidator import InputValidator

class TestValidator(unittest.TestCase):

    def test_valid_string(self):
        self.assertTrue(InputValidator.is_string("Max"))
        self.assertTrue(InputValidator.is_string("Mustermann"))

    def test_invalid_string(self):
        self.assertFalse(InputValidator.is_string(""))
        self.assertFalse(InputValidator.is_string("28"))
        self.assertFalse(InputValidator.is_string("Test28"))
        self.assertFalse(InputValidator.is_string("test@mail.com"))

    def test_valid_number(self):
        self.assertTrue(InputValidator.is_number("1"))
        self.assertTrue(InputValidator.is_number("100"))

    def test_invalid_number(self):
        self.assertFalse(InputValidator.is_number(""))
        self.assertFalse(InputValidator.is_number("H3"))
        self.assertFalse(InputValidator.is_number("21-22"))

    def test_valid_zip_code(self):
        self.assertTrue(InputValidator.is_zip_code("9000"))
        self.assertTrue(InputValidator.is_zip_code("10115"))

    def test_invalid_zip_code(self):
        self.assertFalse(InputValidator.is_zip_code("900"))
        self.assertFalse(InputValidator.is_zip_code("900000"))

    def test_valid_yes_no(self):
        self.assertTrue(InputValidator.is_yes_no("j"))
        self.assertTrue(InputValidator.is_yes_no("J"))
        self.assertTrue(InputValidator.is_yes_no("n"))
        self.assertTrue(InputValidator.is_yes_no("N"))

    def test_invalid_yes_no(self):
        self.assertFalse(InputValidator.is_yes_no("no"))
        self.assertFalse(InputValidator.is_yes_no("yes"))

    def test_valid_mail(self):
        self.assertTrue(InputValidator.is_email("test@mail.com"))

    def test_invalid_mail(self):
        self.assertFalse(InputValidator.is_email("test.com"))
        self.assertFalse(InputValidator.is_email("test@mail"))
        self.assertFalse(InputValidator.is_email("testmail"))

    def test_valid_date_format(self):
        self.assertTrue(InputValidator.is_date("20.12.2000"))
        self.assertTrue(InputValidator.is_date("1.2.2000"))

    def test_invalid_date_forma(self):
        self.assertFalse(InputValidator.is_date("2000-1-2"))
        self.assertFalse(InputValidator.is_date("2000-10-10"))
        self.assertFalse(InputValidator.is_date("2000/1/1"))
        self.assertFalse(InputValidator.is_date("2000/10/21"))


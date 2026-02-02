import re
from datetime import datetime


class InputValidator:
    STRING_PATTERN = re.compile(r"^[a-zA-Z]+$")
    NUMBER_PATTERN = re.compile(r"^[0-9]+$")
    ZIP_CODE_PATTERN = re.compile(r"^[0-9]{4,5}$")
    YES_NO_PATTERN = re.compile(r"^[jJnN]$")
    EMAIL_PATTERN = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )

    @staticmethod
    def is_string(value: str) -> bool:
        return bool(InputValidator.STRING_PATTERN.fullmatch(value))

    @staticmethod
    def is_number(value: str) -> bool:
        return bool(InputValidator.NUMBER_PATTERN.fullmatch(value))

    @staticmethod
    def is_zip_code(value: str) -> bool:
        return bool(InputValidator.ZIP_CODE_PATTERN.fullmatch(value))

    @staticmethod
    def is_yes_no(value: str) -> bool:
        return bool(InputValidator.YES_NO_PATTERN.fullmatch(value))

    @staticmethod
    def is_email(value: str) -> bool:
        return bool(InputValidator.EMAIL_PATTERN.fullmatch(value))

    @staticmethod
    def is_date(value: str) -> bool:
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

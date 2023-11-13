from enum import Enum

from core.system_message_errors.message_user import ValidationModelMessage as V


class ValidateUser(Enum):
    PASSWORD = (r"^[A-Za-z0-9@!#$_\-+]{4,128}$", V.PASSWORD)
    NAME_SURNAME = (
        r"[A-Z][a-z]{2,24}",
        "Fields must have only letters and start with upper",
    )
    MODEL = (
        r"[A-Z][a-z0-9]{2,24}",
        "Fields must have  letters or number and start with upper",
    )

    def __init__(self, pattern, msg):
        self.pattern = pattern
        self.msg = msg

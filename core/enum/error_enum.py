from enum import Enum

from rest_framework import status


class ErrorEnum(Enum):
    JWT = ({"detail": "Token expired or invalid"}, status.HTTP_403_FORBIDDEN)
    BLOCK = ({"detail": "User is block"}, status.HTTP_404_NOT_FOUND)
    PREM = (
        {"detail": "User not have prem and use max advertisement"},
        status.HTTP_403_FORBIDDEN,
    )
    VIEW = (
        {"detail": "User can only send one view"},
        status.HTTP_403_FORBIDDEN,
    )

    def __init__(self, msg, code=status.HTTP_400_BAD_REQUEST):
        self.msg = msg
        self.code = code

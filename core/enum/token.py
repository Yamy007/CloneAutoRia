from datetime import timedelta
from enum import Enum


class TokenEnum(Enum):
    ACTIVATE = ("activate", timedelta(minutes=30))

    def __init__(self, token_type, life_time):
        self.token_type = token_type
        self.life_time = life_time

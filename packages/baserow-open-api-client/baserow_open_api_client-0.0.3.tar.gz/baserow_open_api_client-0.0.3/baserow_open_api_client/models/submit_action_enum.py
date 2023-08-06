from enum import Enum


class SubmitActionEnum(str, Enum):
    MESSAGE = "MESSAGE"
    REDIRECT = "REDIRECT"

    def __str__(self) -> str:
        return str(self.value)

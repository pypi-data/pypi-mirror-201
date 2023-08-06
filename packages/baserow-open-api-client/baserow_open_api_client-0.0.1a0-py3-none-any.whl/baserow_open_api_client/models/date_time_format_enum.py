from enum import Enum


class DateTimeFormatEnum(str, Enum):
    VALUE_0 = "24"
    VALUE_1 = "12"

    def __str__(self) -> str:
        return str(self.value)

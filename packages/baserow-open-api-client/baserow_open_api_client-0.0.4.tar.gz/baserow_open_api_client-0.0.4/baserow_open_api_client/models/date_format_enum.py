from enum import Enum


class DateFormatEnum(str, Enum):
    EU = "EU"
    ISO = "ISO"
    US = "US"

    def __str__(self) -> str:
        return str(self.value)

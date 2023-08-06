from enum import Enum


class ModeEnum(str, Enum):
    FORM = "form"
    SURVEY = "survey"

    def __str__(self) -> str:
        return str(self.value)

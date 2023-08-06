from enum import Enum


class Type20DEnum(str, Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class ArrayFormulaTypeEnum(str, Enum):
    BOOLEAN = "boolean"
    CHAR = "char"
    DATE = "date"
    DATE_INTERVAL = "date_interval"
    INVALID = "invalid"
    LINK = "link"
    NUMBER = "number"
    SINGLE_SELECT = "single_select"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)

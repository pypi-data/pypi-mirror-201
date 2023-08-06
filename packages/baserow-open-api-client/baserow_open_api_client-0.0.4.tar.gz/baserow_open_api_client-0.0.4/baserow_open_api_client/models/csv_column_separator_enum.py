from enum import Enum


class CsvColumnSeparatorEnum(str, Enum):
    RECORD_SEPARATOR = "record_separator"
    TAB = "tab"
    UNIT_SEPARATOR = "unit_separator"
    VALUE_0 = ","
    VALUE_1 = ";"
    VALUE_2 = "|"

    def __str__(self) -> str:
        return str(self.value)

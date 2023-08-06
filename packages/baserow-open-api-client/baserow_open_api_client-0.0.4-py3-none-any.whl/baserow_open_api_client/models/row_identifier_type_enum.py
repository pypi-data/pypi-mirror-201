from enum import Enum


class RowIdentifierTypeEnum(str, Enum):
    COUNT = "count"
    ID = "id"

    def __str__(self) -> str:
        return str(self.value)

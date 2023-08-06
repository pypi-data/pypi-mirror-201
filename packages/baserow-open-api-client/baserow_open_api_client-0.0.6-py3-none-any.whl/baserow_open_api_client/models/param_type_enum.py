from enum import Enum


class ParamTypeEnum(str, Enum):
    NUMERIC = "numeric"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)

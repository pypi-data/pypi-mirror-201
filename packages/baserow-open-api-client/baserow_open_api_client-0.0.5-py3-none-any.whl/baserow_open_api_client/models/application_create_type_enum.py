from enum import Enum


class ApplicationCreateTypeEnum(str, Enum):
    BUILDER = "builder"
    DATABASE = "database"

    def __str__(self) -> str:
        return str(self.value)

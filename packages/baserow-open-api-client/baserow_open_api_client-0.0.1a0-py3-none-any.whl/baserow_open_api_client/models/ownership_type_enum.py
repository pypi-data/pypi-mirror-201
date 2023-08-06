from enum import Enum


class OwnershipTypeEnum(str, Enum):
    COLLABORATIVE = "collaborative"
    PERSONAL = "personal"

    def __str__(self) -> str:
        return str(self.value)

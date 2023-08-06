from enum import Enum


class SubjectType3FfEnum(str, Enum):
    AUTH_USER = "auth.User"

    def __str__(self) -> str:
        return str(self.value)

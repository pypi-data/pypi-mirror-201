from enum import Enum


class UpdateDatabaseTokenResponse404Error(str, Enum):
    ERROR_TOKEN_DOES_NOT_EXIST = "ERROR_TOKEN_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)

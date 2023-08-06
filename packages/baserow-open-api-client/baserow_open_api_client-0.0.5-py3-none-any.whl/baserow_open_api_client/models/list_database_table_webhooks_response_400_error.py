from enum import Enum


class ListDatabaseTableWebhooksResponse400Error(str, Enum):
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)

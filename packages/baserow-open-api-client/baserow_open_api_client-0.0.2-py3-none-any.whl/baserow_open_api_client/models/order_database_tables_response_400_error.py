from enum import Enum


class OrderDatabaseTablesResponse400Error(str, Enum):
    ERROR_TABLE_NOT_IN_DATABASE = "ERROR_TABLE_NOT_IN_DATABASE"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)

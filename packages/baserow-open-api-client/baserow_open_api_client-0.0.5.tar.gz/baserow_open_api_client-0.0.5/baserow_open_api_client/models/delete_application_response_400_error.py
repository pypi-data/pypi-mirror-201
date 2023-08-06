from enum import Enum


class DeleteApplicationResponse400Error(str, Enum):
    ERROR_CANNOT_DELETE_ALREADY_DELETED_ITEM = "ERROR_CANNOT_DELETE_ALREADY_DELETED_ITEM"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)

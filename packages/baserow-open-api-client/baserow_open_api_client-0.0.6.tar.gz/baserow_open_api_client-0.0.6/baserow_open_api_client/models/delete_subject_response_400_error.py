from enum import Enum


class DeleteSubjectResponse400Error(str, Enum):
    ERROR_CANNOT_DELETE_ALREADY_DELETED_ITEM = "ERROR_CANNOT_DELETE_ALREADY_DELETED_ITEM"

    def __str__(self) -> str:
        return str(self.value)

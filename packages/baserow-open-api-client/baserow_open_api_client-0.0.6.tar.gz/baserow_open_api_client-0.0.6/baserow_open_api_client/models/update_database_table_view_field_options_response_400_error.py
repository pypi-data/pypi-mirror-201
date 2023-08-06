from enum import Enum


class UpdateDatabaseTableViewFieldOptionsResponse400Error(str, Enum):
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"
    ERROR_VIEW_DOES_NOT_SUPPORT_FIELD_OPTIONS = "ERROR_VIEW_DOES_NOT_SUPPORT_FIELD_OPTIONS"

    def __str__(self) -> str:
        return str(self.value)

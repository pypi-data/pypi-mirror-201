from enum import Enum


class WorkspaceEmptyContentsResponse400Error(str, Enum):
    ERROR_APPLICATION_DOES_NOT_EXIST = "ERROR_APPLICATION_DOES_NOT_EXIST"
    ERROR_APPLICATION_NOT_IN_GROUP = "ERROR_APPLICATION_NOT_IN_GROUP"
    ERROR_GROUP_DOES_NOT_EXIST = "ERROR_GROUP_DOES_NOT_EXIST"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)

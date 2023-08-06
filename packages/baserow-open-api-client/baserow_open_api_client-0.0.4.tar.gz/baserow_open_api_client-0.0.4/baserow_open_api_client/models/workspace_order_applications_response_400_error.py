from enum import Enum


class WorkspaceOrderApplicationsResponse400Error(str, Enum):
    ERROR_APPLICATION_NOT_IN_GROUP = "ERROR_APPLICATION_NOT_IN_GROUP"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)

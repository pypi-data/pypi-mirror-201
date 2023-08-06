from enum import Enum


class DuplicateApplicationAsyncResponse400Error(str, Enum):
    ERROR_APPLICATION_NOT_IN_GROUP = "ERROR_APPLICATION_NOT_IN_GROUP"
    ERROR_MAX_JOB_COUNT_EXCEEDED = "ERROR_MAX_JOB_COUNT_EXCEEDED"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)

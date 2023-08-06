from enum import Enum


class CreateDatabaseTableAsyncResponse400Error(str, Enum):
    ERROR_MAX_JOB_COUNT_EXCEEDED = "ERROR_MAX_JOB_COUNT_EXCEEDED"
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)

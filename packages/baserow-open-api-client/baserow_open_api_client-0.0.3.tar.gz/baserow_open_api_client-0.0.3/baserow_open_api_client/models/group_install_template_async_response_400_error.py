from enum import Enum


class GroupInstallTemplateAsyncResponse400Error(str, Enum):
    ERROR_MAX_JOB_COUNT_EXCEEDED = "ERROR_MAX_JOB_COUNT_EXCEEDED"
    ERROR_TEMPLATE_FILE_DOES_NOT_EXIST = "ERROR_TEMPLATE_FILE_DOES_NOT_EXIST"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class GroupInstallTemplateResponse400Error(str, Enum):
    ERROR_TEMPLATE_FILE_DOES_NOT_EXIST = "ERROR_TEMPLATE_FILE_DOES_NOT_EXIST"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)

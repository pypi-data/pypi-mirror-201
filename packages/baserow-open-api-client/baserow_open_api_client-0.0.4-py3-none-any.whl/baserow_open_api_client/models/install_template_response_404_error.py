from enum import Enum


class InstallTemplateResponse404Error(str, Enum):
    ERROR_GROUP_DOES_NOT_EXIST = "ERROR_GROUP_DOES_NOT_EXIST"
    ERROR_TEMPLATE_DOES_NOT_EXIST = "ERROR_TEMPLATE_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)

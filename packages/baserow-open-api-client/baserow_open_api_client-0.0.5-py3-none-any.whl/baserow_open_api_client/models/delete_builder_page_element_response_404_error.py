from enum import Enum


class DeleteBuilderPageElementResponse404Error(str, Enum):
    ERROR_ELEMENT_DOES_NOT_EXIST = "ERROR_ELEMENT_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)

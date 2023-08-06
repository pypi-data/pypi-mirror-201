from enum import Enum


class CreateBuilderPageElementResponse404Error(str, Enum):
    ERROR_PAGE_DOES_NOT_EXIST = "ERROR_PAGE_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)

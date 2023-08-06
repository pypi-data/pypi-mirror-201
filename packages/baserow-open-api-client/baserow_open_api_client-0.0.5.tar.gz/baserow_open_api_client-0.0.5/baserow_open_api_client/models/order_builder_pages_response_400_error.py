from enum import Enum


class OrderBuilderPagesResponse400Error(str, Enum):
    ERROR_PAGE_NOT_IN_BUILDER = "ERROR_PAGE_NOT_IN_BUILDER"
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"

    def __str__(self) -> str:
        return str(self.value)

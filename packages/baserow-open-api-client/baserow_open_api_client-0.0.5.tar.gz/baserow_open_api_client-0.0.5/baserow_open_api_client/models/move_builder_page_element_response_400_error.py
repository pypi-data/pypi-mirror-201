from enum import Enum


class MoveBuilderPageElementResponse400Error(str, Enum):
    ERROR_ELEMENT_NOT_IN_SAME_PAGE = "ERROR_ELEMENT_NOT_IN_SAME_PAGE"
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"

    def __str__(self) -> str:
        return str(self.value)

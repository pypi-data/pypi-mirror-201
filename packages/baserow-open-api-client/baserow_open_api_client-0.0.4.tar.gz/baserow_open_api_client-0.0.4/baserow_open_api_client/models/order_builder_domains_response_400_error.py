from enum import Enum


class OrderBuilderDomainsResponse400Error(str, Enum):
    ERROR_DOMAIN_NOT_IN_BUILDER = "ERROR_DOMAIN_NOT_IN_BUILDER"
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class CreateBuilderDomainResponse400Error(str, Enum):
    ERROR_ONLY_ONE_DOMAIN_ALLOWED = "ERROR_ONLY_ONE_DOMAIN_ALLOWED"
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class DeleteBuilderDomainResponse404Error(str, Enum):
    ERROR_DOMAIN_DOES_NOT_EXIST = "ERROR_DOMAIN_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)

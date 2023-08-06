from enum import Enum


class OrderBuilderDomainsResponse404Error(str, Enum):
    ERROR_APPLICATION_DOES_NOT_EXIST = "ERROR_APPLICATION_DOES_NOT_EXIST"
    ERROR_DOMAIN_DOES_NOT_EXIST = "ERROR_DOMAIN_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)

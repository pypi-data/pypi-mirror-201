from enum import Enum


class GetAuthProviderResponse404Error(str, Enum):
    ERROR_AUTH_PROVIDER_DOES_NOT_EXIST = "ERROR_AUTH_PROVIDER_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)

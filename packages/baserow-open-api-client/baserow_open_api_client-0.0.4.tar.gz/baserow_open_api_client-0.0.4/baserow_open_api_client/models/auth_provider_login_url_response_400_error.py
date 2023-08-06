from enum import Enum


class AuthProviderLoginUrlResponse400Error(str, Enum):
    ERROR_SAML_INVALID_LOGIN_REQUEST = "ERROR_SAML_INVALID_LOGIN_REQUEST"

    def __str__(self) -> str:
        return str(self.value)

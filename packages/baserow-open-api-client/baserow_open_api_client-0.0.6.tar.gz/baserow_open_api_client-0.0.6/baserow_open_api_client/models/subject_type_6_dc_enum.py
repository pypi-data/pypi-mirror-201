from enum import Enum


class SubjectType6DcEnum(str, Enum):
    ANONYMOUS = "anonymous"
    AUTH_USER = "auth.User"
    BASEROW_ENTERPRISE_TEAM = "baserow_enterprise.Team"
    CORE_TOKEN = "core.Token"

    def __str__(self) -> str:
        return str(self.value)

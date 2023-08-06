from enum import Enum


class CreateDatabaseTableWebhookResponse400Error(str, Enum):
    ERROR_TABLE_WEBHOOK_MAX_LIMIT_EXCEEDED = "ERROR_TABLE_WEBHOOK_MAX_LIMIT_EXCEEDED"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)

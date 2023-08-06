from enum import Enum


class TestCallDatabaseTableWebhookResponse404Error(str, Enum):
    ERROR_TABLE_DOES_NOT_EXIST = "ERROR_TABLE_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)

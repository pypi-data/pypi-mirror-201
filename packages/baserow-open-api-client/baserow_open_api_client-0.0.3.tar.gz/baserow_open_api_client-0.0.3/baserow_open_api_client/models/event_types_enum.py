from enum import Enum


class EventTypesEnum(str, Enum):
    ROWS_CREATED = "rows.created"
    ROWS_DELETED = "rows.deleted"
    ROWS_UPDATED = "rows.updated"

    def __str__(self) -> str:
        return str(self.value)

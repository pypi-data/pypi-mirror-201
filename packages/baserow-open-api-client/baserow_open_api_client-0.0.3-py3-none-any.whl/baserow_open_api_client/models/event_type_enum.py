from enum import Enum


class EventTypeEnum(str, Enum):
    ROWS_CREATED = "rows.created"
    ROWS_DELETED = "rows.deleted"
    ROWS_UPDATED = "rows.updated"
    ROW_CREATED = "row.created"
    ROW_DELETED = "row.deleted"
    ROW_UPDATED = "row.updated"

    def __str__(self) -> str:
        return str(self.value)

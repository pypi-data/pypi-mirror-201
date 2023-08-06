from enum import Enum


class ListDatabaseTableCalendarViewRowsResponse400Error(str, Enum):
    ERROR_CALENDAR_VIEW_HAS_NO_DATE_FIELD = "ERROR_CALENDAR_VIEW_HAS_NO_DATE_FIELD"
    ERROR_FEATURE_NOT_AVAILABLE = "ERROR_FEATURE_NOT_AVAILABLE"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)

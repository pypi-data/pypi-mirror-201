from enum import Enum


class PublicListDatabaseTableKanbanViewRowsResponse400Error(str, Enum):
    ERROR_INVALID_SELECT_OPTION_PARAMETER = "ERROR_INVALID_SELECT_OPTION_PARAMETER"
    ERROR_KANBAN_VIEW_HAS_NO_SINGLE_SELECT_FIELD = "ERROR_KANBAN_VIEW_HAS_NO_SINGLE_SELECT_FIELD"

    def __str__(self) -> str:
        return str(self.value)

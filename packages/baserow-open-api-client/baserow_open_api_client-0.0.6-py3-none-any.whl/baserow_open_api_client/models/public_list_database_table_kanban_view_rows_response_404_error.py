from enum import Enum


class PublicListDatabaseTableKanbanViewRowsResponse404Error(str, Enum):
    ERROR_KANBAN_DOES_NOT_EXIST = "ERROR_KANBAN_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)

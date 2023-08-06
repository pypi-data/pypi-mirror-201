from enum import Enum


class ViewTypesEnum(str, Enum):
    CALENDAR = "calendar"
    FORM = "form"
    GALLERY = "gallery"
    GRID = "grid"
    KANBAN = "kanban"

    def __str__(self) -> str:
        return str(self.value)

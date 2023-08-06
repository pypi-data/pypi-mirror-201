from enum import Enum


class TrashItemTypeEnum(str, Enum):
    APPLICATION = "application"
    FIELD = "field"
    GROUP = "group"
    ROW = "row"
    ROWS = "rows"
    TABLE = "table"
    TEAM = "team"
    VIEW = "view"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)

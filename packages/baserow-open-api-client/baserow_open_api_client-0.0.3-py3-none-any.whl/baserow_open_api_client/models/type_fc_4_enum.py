from enum import Enum


class TypeFc4Enum(str, Enum):
    BACKGROUND_COLOR = "background_color"
    LEFT_BORDER_COLOR = "left_border_color"

    def __str__(self) -> str:
        return str(self.value)

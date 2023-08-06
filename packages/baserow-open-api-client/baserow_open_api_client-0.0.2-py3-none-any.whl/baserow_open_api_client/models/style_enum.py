from enum import Enum


class StyleEnum(str, Enum):
    FLAG = "flag"
    HEART = "heart"
    SMILE = "smile"
    STAR = "star"
    THUMBS_UP = "thumbs-up"

    def __str__(self) -> str:
        return str(self.value)

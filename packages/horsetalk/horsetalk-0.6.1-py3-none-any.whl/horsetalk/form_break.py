from enum import Enum


class FormBreak(Enum):
    YEAR = "-"
    SEASON = "/"

    def __str__(self):
        return self.value

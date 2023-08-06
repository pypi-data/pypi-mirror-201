from enum import Enum
from .case_insensitive_enum import CaseInsensitiveEnumMeta


class ObstacleEnumMeta(CaseInsensitiveEnumMeta):
    def __getitem__(cls, name):
        return super().__getitem__(name.replace("-", " ").replace(" ", "_"))


class Obstacle(Enum, metaclass=ObstacleEnumMeta):
    """
    An enumeration representing the type of obstacle a race takes place over
    """

    HURDLE = 1
    STEEPLECHASE = 2
    CROSS_COUNTRY = 3

    # Abbreviations
    H = HURDLE
    HRD = HURDLE
    HRDLE = HURDLE
    C = STEEPLECHASE
    CH = STEEPLECHASE
    CHS = STEEPLECHASE
    CHSE = STEEPLECHASE
    CHASE = STEEPLECHASE
    CC = CROSS_COUNTRY
    XC = CROSS_COUNTRY

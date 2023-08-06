from .case_insensitive_enum import CaseInsensitiveEnum


class CoatColour(CaseInsensitiveEnum):
    """
    An enumeration representing a coat colour of a horse.
    """

    BAY = 1
    BLACK = 2
    CHESTNUT = 3
    DARK_BAY = 4
    GREY = 5
    PALOMINO = 6
    WHITE = 7

    # Abbreviations
    B = BAY
    BL = BLACK
    C = CHESTNUT
    CH = CHESTNUT
    DB = DARK_BAY
    BR = DARK_BAY
    G = GREY
    GR = GREY
    GRAY = GREY
    P = PALOMINO
    W = WHITE

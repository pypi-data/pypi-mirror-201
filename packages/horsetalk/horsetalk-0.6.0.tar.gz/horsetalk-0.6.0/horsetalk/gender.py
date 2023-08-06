from .parsing_enum import ParsingEnum


class Gender(ParsingEnum):
    """
    An enumeration representing the gender of a horse
    """

    FOAL = 0
    YEARLING = 1
    COLT = 2
    FILLY = 3
    STALLION = 4
    MARE = 5
    GELDING = 6
    RIG = 7

    # Abbreviations
    C = COLT
    F = FILLY
    S = STALLION
    M = MARE
    G = GELDING
    R = RIG

    # Plural
    FOALS = FOAL
    YEARLINGS = YEARLING
    COLTS = COLT
    FILLIES = FILLY
    STALLIONS = STALLION
    MARES = MARE
    GELDINGS = GELDING
    RIGS = RIG

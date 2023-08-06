from .parsing_enum import ParsingEnum


class RaceDesignation(ParsingEnum):
    HANDICAP = 1
    CONDITIONS = 2
    AUCTION = 3
    CLAIMER = 4
    SELLER = 5

    # Abbreviations
    HCAP = HANDICAP
    AU = AUCTION
    CL = CLAIMER
    S = SELLER

    # Alternatives
    CLAIMING = CLAIMER
    SELLING = SELLER

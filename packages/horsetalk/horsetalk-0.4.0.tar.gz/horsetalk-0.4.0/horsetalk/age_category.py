from .parsing_enum import ParsingEnum


class AgeCategory(ParsingEnum):
    JUVENILE = 1
    VETERAN = 2

    # Alternatives
    VETERANS = VETERAN

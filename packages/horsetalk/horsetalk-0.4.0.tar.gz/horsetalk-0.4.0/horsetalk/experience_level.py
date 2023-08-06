from .parsing_enum import ParsingEnum


class ExperienceLevel(ParsingEnum):
    MAIDEN = 1
    NOVICE = 2
    BEGINNER = 3

    # Alternatives
    NOVICES = NOVICE
    BEGINNERS = BEGINNER

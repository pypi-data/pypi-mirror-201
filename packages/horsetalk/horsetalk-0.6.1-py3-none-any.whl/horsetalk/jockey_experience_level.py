from .parsing_enum import ParsingEnum


class JockeyExperienceLevel(ParsingEnum):
    AMATEUR = 1
    CONDITIONAL = 2
    APPRENTICE = 3
    PROFESSIONAL = 4

    # Plurals
    AMATEURS = AMATEUR
    CONDITIONALS = CONDITIONAL
    APPRENTICES = APPRENTICE
    PROFESSIONALS = PROFESSIONAL

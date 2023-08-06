from enum import Enum
from typing import List, Type
from .age_category import AgeCategory
from .experience_level import ExperienceLevel
from .gender import Gender
from .obstacle import Obstacle
from .weight_determinant import WeightDeterminant


class RaceTitle:
    _words: List[str] = []

    @classmethod
    def parse(cls, title: str) -> dict:
        """Parse a race title into component parts

        :param title: A race title
        :type title: str
        :return: A dictionary of component parts
        :rtype: dict
        """
        self = cls()
        self._words = title.split()

        enums = [AgeCategory, ExperienceLevel, Gender, Obstacle, WeightDeterminant]
        end_index = -1
        for i, word in enumerate(self._words):
            if any(getattr(enum, word, None) is not None for enum in enums):
                end_index = i
                break
        name = " ".join(self._words[:end_index])

        return {
            "age_category": self._lookup(AgeCategory),
            "experience_level": self._lookup(ExperienceLevel),
            "gender": self._lookup(Gender, allow_multiple=True),
            "obstacle": self._lookup(Obstacle),
            "weight_determinant": self._lookup(WeightDeterminant),
            "name": name,
        }

    def _lookup(
        self, enum: Type[Enum], allow_multiple: bool = False
    ) -> List[Enum] | Enum | None:
        """Private method to lookup an enum value from a list of words

        :param enum: Enum to search through
        :type enum: Type[Enum]
        :return: The found Enum value or None
        :rtype: Enum | None
        """
        found_values = [
            found_value
            for word in self._words
            if (found_value := getattr(enum, word, None)) is not None
        ]
        return (
            None
            if not found_values
            else found_values
            if allow_multiple
            else found_values[-1]
        )

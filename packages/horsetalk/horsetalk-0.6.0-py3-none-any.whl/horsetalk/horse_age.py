from typing import Self
import pendulum
from pendulum import DateTime, Period


class HorseAge:
    def __init__(
        self,
        official_age: int | None = None,
        *,
        foaling_date: DateTime | None = None,
        birth_year: int | None = None,
        context_date: DateTime | None = None
    ):
        if official_age is not None and (foaling_date or birth_year):
            raise ValueError(
                "Cannot initialize HorseAge with both official_age and keyword"
            )

        if not (official_age or foaling_date or birth_year):
            raise ValueError(
                "Cannot initialize HorseAge without official_age, foaling_date, or birth_year"
            )

        self._actual_dob = foaling_date
        self._context_date = context_date

        year = (
            birth_year
            if birth_year
            else self._base_date.year - official_age
            if official_age
            else foaling_date.year
            if foaling_date
            else None
        )

        self._official_dob = pendulum.datetime(year, 1, 1) if year else None

    @property
    def official(self) -> Period:
        if not self._official_dob:
            raise ValueError("Cannot calculate official age as official dob is unknown")
        return self._calc_age(self._official_dob)

    @property
    def actual(self) -> Period:
        if not self._actual_dob:
            raise ValueError("Cannot calculate actual age as actual dob is unknown")
        return self._calc_age(self._actual_dob)

    @property
    def _base_date(self) -> DateTime:
        return self._context_date if self._context_date else pendulum.now()

    def at(self, date: DateTime) -> Self:
        self._context_date = date
        return self

    def _calc_age(self, dob: DateTime) -> Period:
        return (
            self._base_date - dob
            if dob < self._base_date
            else self._base_date - self._base_date
        )

from enum import Enum
from .case_insensitive_enum import CaseInsensitiveEnumMeta


class DisasterEnumMeta(CaseInsensitiveEnumMeta):
    def __getitem__(cls, name):
        return super().__getitem__(name.replace(" ", "_"))


class Disaster(Enum, metaclass=DisasterEnumMeta):
    """
    An enumeration representing the reason for a horse's non-completion of a race
    """

    FELL = 1
    REFUSED = 2
    BROUGHT_DOWN = 3
    UNSEATED_RIDER = 4
    PULLED_UP = 5
    SLIPPED_UP = 6
    CARRIED_OUT = 7
    RAN_OUT = 8
    LEFT_AT_START = 9
    HIT_RAIL = 10
    DISQUALIFIED = 11

    # Abbreviations
    F = FELL
    R = REFUSED
    REF = REFUSED
    B = BROUGHT_DOWN
    BD = BROUGHT_DOWN
    U = UNSEATED_RIDER
    UR = UNSEATED_RIDER
    P = PULLED_UP
    PU = PULLED_UP
    S = SLIPPED_UP
    SU = SLIPPED_UP
    C = CARRIED_OUT
    CO = CARRIED_OUT
    O = RAN_OUT
    RO = RAN_OUT
    L = LEFT_AT_START
    LEFT = LEFT_AT_START
    HR = HIT_RAIL
    D = DISQUALIFIED
    DQ = DISQUALIFIED
    DSQ = DISQUALIFIED

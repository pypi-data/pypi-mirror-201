from enum import Enum, EnumMeta


class CaseInsensitiveEnumMeta(EnumMeta):
    def __getitem__(cls, name):
        for member in cls.__members__:
            if member == name.upper():
                return cls.__members__[member]
        raise KeyError(name)


class CaseInsensitiveEnum(Enum, metaclass=CaseInsensitiveEnumMeta):
    pass

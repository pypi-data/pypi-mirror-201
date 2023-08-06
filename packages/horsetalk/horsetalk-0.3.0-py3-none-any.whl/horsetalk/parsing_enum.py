from enum import Enum, EnumMeta


class ParsingEnumMeta(EnumMeta):
    def __getitem__(cls, name):
        for member in cls.__members__:
            if member == name.replace("-", " ").replace(" ", "_").upper():
                return cls.__members__[member]
        raise KeyError(name)


class ParsingEnum(Enum, metaclass=ParsingEnumMeta):
    pass

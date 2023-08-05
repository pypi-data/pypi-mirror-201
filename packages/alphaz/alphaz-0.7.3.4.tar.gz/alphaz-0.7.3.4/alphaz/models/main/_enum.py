from enum import Enum


class AlphaEnum(Enum):
    def __str__(self):
        return str(self.value)

    def to_json(self):
        return str(self.value)


class EnumStr(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class MappingMode(AlphaEnum):
    AUTO1 = "auto1"
    STRICT1 = "strict1"

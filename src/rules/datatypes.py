from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name.title()) for key in cls]

    def __str__(self):
        return self.value

    @classmethod
    def has_value(cls, value):
        return value.lower() in [key.value.lower() for key in cls]

    @classmethod
    def has_key(cls, key):
        return key.lower() in [key.name.lower() for key in cls]


class ConditionOperator(BaseEnum):
    GREATER_THAN = (">", "gt")
    GREATER_THAN_OR_EQUAL_TO = (">=", "gte")
    LESS_THAN = ("<", "lt")
    LESS_THAN_OR_EQUAL_TO = ("=<", "lte")
    ALL = ("all", "all")
    ANY = ("any", "any")

    @classmethod
    def choices(cls):
        return [(key.value[1], key.value[0]) for key in cls]

    @classmethod
    def has_value(cls, value):
        return value.lower() in [key.value[1].lower() for key in cls]


class ConditionAttribute(BaseEnum):
    AGE = "Age"
    SYMPTOMS = "Symptoms"
    RISK_FACTORS = "Risk Factors"
    ENCOUNTER_DISTANCE = "Encounter Distance"
    ENCOUNTER_DURATION = "Encounter Duration"

    @classmethod
    def choices(cls):
        return [(key.name.lower(), key.value) for key in cls]

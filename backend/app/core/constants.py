from enum import Enum


class AcceptedTypes(Enum):
    NUMERIC = "numeric"
    STRING = "string"
    DATETIME = "datetime"
    BOOLEAN = "boolean"


class FilterOperator(Enum):
    EQUAL = "eq"
    NOT_EQUAL = "ne"
    GREATER = "gt"
    GREATER_EQUAL = "ge"
    LESS = "lt"
    LESS_EQUAL = "le"
    BETWEEN = "between"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    STARTSWITH = "startswith"
    ENDSWITH = "endswith"
    IS_IN = "in"
    IS_NOT_IN = "not_in"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"
    IDENTITY = "identity"


class CompositionOperator(Enum):
    AND = "and"
    OR = "or"
    NOT = "not"

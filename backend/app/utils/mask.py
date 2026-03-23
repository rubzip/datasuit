from abc import abstractmethod
from typing import List, Any, Dict, Type
import pandas as pd
from core.constants import AcceptedTypes
from utils.base import BaseAction

class Mask(BaseAction):
    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        raise NotImplementedError

class ColumnMask(Mask):
    """Works over a columns"""
    def __init__(self, column: str, value: Any):
        self.column = column
        self.value = value
    
    def get_used_columns(self) -> set[str]:
        return {self.column}

# -- Comparison Filters --

class ComparisonMask(ColumnMask):
    SYMBOL = ""
    def __init__(self, column: str, value: Any):
        super().__init__(column, value)
    
    def to_code(self):
        return f"df['{self.column}'] {self.SYMBOL} {self.value}"

class EqualMask(ComparisonMask):
    SYMBOL = "=="
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] == self.value


class NotEqualMask(ComparisonMask):
    SYMBOL = "!="
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] != self.value


class GreaterMask(ComparisonMask):
    SYMBOL = ">"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] > self.value


class GreaterEqualMask(ComparisonMask):
    SYMBOL = ">="
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] >= self.value


class LessMask(ComparisonMask):
    SYMBOL = "<"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] < self.value


class LessEqualMask(ComparisonMask):
    SYMBOL = "<="
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] <= self.value


# -- Null Filters --
class NoValueMask(ColumnMask):
    METHOD =  ""
    def __init__(self, column, value = None):
        super().__init__(column, value)
    
    def to_code(self) -> str:
        return f"df['{self.column}'].{self.METHOD}()"

class IsNullMask(NoValueMask):
    METHOD = "isnull"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].isnull()


class IsNotNullMask(NoValueMask):
    METHOD = "notnull"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].notnull()


# -- String Filters --


class StringMask(ColumnMask):
    METHOD = ""
    def __init__(self, column: str, value: str):
        super().__init__(column=column, value=value)

    def __str__(self):
        return f"df['{self.column}'].str.{self.METHOD}('{self.value}')"

class ContainsMask(StringMask):
    METHOD = "contains"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].str.contains(self.value)


class NotContainsMask(StringMask):
    METHOD = "contains"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return ~df[self.column].str.contains(self.value)

    def __str__(self):
        return f"~df['{self.column}'].str.{self.METHOD}('{self.value}')"


class StartsWithMask(StringMask):
    METHOD = "startswith"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].str.startswith(self.value)


class EndsWithMask(StringMask):
    METHOD = "endswith"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].str.endswith(self.value)


# -- Membership Filters --

class MembershipMask(ColumnMask):
    NEGATION = ""
    def __init__(self, column: str, value: List[Any]):
        super().__init__(column, value)
    
    def to_code(self) -> str:
        return f"{self.NEGATION}df['{self.column}'].isin({self.value})"

class IsInMask(MembershipMask):
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].isin(self.value)

class IsNotInMask(MembershipMask):
    NEGATION = "~"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return ~df[self.column].isin(self.value)

# -- Binary Masks --

class BinaryMask(Mask):
    SYMBOL = ""
    def __init__(self, left: Mask, right: Mask):
        self.left = left
        self.right = right
    
    def to_code(self):
        left_str = f"({self.left})" if isinstance(self.left, BinaryMask) else str(self.left)
        right_str = f"({self.right})" if isinstance(self.right, BinaryMask) else str(self.right)
        
        return f"{left_str} {self.SYMBOL} {right_str}"
    
    def get_used_columns(self) -> set[str]:
        return self.left.get_used_columns().union(self.right.get_used_columns())

class AndMask(BinaryMask):
    SYMBOL = "&"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return self.left.apply(df) & self.right.apply(df)

class OrMask(BinaryMask):
    SYMBOL = "|"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return self.left.apply(df) | self.right.apply(df)

# -- Unary Masks --

class NotMask(BinaryMask):
    SYMBOL = "~"
    def __init__(self, left: Mask, right: Mask = None):
        self.left = left
    
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return ~self.left.apply(df)
    
    def to_code(self):
        left_str = f"({self.left})" if isinstance(self.left, BinaryMask) else str(self.left)
        return f"{self.SYMBOL} {left_str}"
    
    def get_used_columns(self) -> set[str]:
        return self.left.get_used_columns()


from app.core.constants import FilterOperator, CompositionOperator

MAPPER_MASK = {
    FilterOperator.EQUAL: EqualMask,
    FilterOperator.NOT_EQUAL: NotEqualMask,
    FilterOperator.GREATER: GreaterMask,
    FilterOperator.GREATER_EQUAL: GreaterEqualMask,
    FilterOperator.LESS: LessMask,
    FilterOperator.LESS_EQUAL: LessEqualMask,
    FilterOperator.IS_NULL: IsNullMask,
    FilterOperator.IS_NOT_NULL: IsNotNullMask,
    FilterOperator.CONTAINS: ContainsMask,
    FilterOperator.NOT_CONTAINS: NotContainsMask,
    FilterOperator.STARTSWITH: StartsWithMask,
    FilterOperator.ENDSWITH: EndsWithMask,
    FilterOperator.IS_IN: IsInMask,
    FilterOperator.IS_NOT_IN: IsNotInMask,
    FilterOperator.IDENTITY: IdentityMask,
}

MAPPER_COMPOSITION = {
    CompositionOperator.AND: AndMask,
    CompositionOperator.OR: OrMask,
    CompositionOperator.NOT: NotMask,
}

from typing import Any, Union
import datetime
from app.schemas import FilterCondition, ComposedFilterCondition, TypedValue


def cast(value: Union[TypedValue, List[TypedValue]]) -> Any:
    if isinstance(value, list):
        return [cast(v) for v in value]
    if not isinstance(value, TypedValue):
        return value
    if value.type == AcceptedTypes.NUMERIC:
        return float(value.value)
    if value.type == AcceptedTypes.STRING:
        return str(value.value)
    if value.type == AcceptedTypes.DATETIME:
        return datetime.fromisoformat(value.value)
    if value.type == AcceptedTypes.BOOLEAN:
        return bool(value.value)
    raise NotImplementedError(f"Invalid type: {value.type}")


def get_mask(f: Union[FilterCondition, ComposedFilterCondition]) -> BaseMask:
    if isinstance(f, ComposedFilterCondition):
        return MAPPER_COMPOSITION.get(f.operator)(
            left=get_mask(f.left_condition),
            right=get_mask(f.right_condition)
        )
    if isinstance(f, FilterCondition):
        return MAPPER_MASK.get(f.operator)(
            column=f.column,
            value=cast(f.value)
        )
    raise ValueError(f"Invalid filter operator: {f}")

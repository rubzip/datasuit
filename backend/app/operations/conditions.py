from typing import Any, List
import pandas as pd
from app.operations.base import Condition
from app.core.constants import AcceptedTypes


class ColumnCondition(Condition):
    """Works over a columns"""

    def __init__(self, column: str, value: Any = None):
        self.column = column
        self.value = value

    def get_used_columns(self) -> set[str]:
        return {self.column}


class LogicalCondition(Condition):
    SYMBOL = ""

    def __init__(self, left: Condition, right: Condition = None):
        self.left = left
        self.right = right

    def to_code(self) -> str:
        left_str = f"({self.left.to_code()})"
        if self.right:
            right_str = f"({self.right.to_code()})"
            return f"{left_str} {self.SYMBOL} {right_str}"
        return f"{self.SYMBOL} {left_str}"

    def get_used_columns(self) -> set[str]:
        cols = self.left.get_used_columns()
        if self.right:
            cols = cols.union(self.right.get_used_columns())
        return cols


# -- Comparison Conditions --


class ComparisonCondition(ColumnCondition):
    SYMBOL = ""

    def __init__(self, column: str, value: Any):
        super().__init__(column, value)

    def to_code(self) -> str:
        return f"df['{self.column}'] {self.SYMBOL} {self.value}"


class EqualsCondition(ComparisonCondition):
    SYMBOL = "=="

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] == self.value


class NotEqualsCondition(ComparisonCondition):
    SYMBOL = "!="

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] != self.value


class GreaterThanCondition(ComparisonCondition):
    SYMBOL = ">"

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] > self.value


class GreaterThanOrEqualsCondition(ComparisonCondition):
    SYMBOL = ">="

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] >= self.value


class LessThanCondition(ComparisonCondition):
    SYMBOL = "<"

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] < self.value


class LessThanOrEqualsCondition(ComparisonCondition):
    SYMBOL = "<="

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] <= self.value


# -- Nullability Conditions --


class NullabilityCondition(ColumnCondition):
    METHOD = ""

    def __init__(self, column: str, value: Any = None):
        super().__init__(column, value)

    def to_code(self) -> str:
        return f"df['{self.column}'].{self.METHOD}()"


class IdentityCondition(ColumnCondition):
    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column]

    def to_code(self) -> str:
        return f"df['{self.column}']"


class IsNullCondition(NullabilityCondition):
    METHOD = "isnull"

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].isnull()


class IsNotNullCondition(NullabilityCondition):
    METHOD = "notnull"

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].notnull()


# -- String Conditions --


class StringCondition(ColumnCondition):
    METHOD = ""

    def __init__(self, column: str, value: str):
        super().__init__(column=column, value=value)

    def to_code(self) -> str:
        return f"df['{self.column}'].str.{self.METHOD}('{self.value}')"


class ContainsCondition(StringCondition):
    METHOD = "contains"

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].str.contains(self.value)


class StartsWithCondition(StringCondition):
    METHOD = "startswith"

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].str.startswith(self.value)


class EndsWithCondition(StringCondition):
    METHOD = "endswith"

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].str.endswith(self.value)


# -- Membership Conditions --


class MembershipCondition(ColumnCondition):
    NEGATION = ""

    def __init__(self, column: str, value: List[Any]):
        super().__init__(column, value)

    def to_code(self) -> str:
        return f"{self.NEGATION}df['{self.column}'].isin({self.value})"


class InCondition(MembershipCondition):
    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].isin(self.value)


# -- Logical Conditions --


class AndCondition(LogicalCondition):
    SYMBOL = "&"

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return self.left.apply(df) & self.right.apply(df)


class OrCondition(LogicalCondition):
    SYMBOL = "|"

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return self.left.apply(df) | self.right.apply(df)


class NotCondition(LogicalCondition):
    SYMBOL = "~"

    def __init__(self, left: Condition, right: Condition = None):
        super().__init__(left, right)

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return ~self.left.apply(df)

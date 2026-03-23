from typing import List, Any
import pandas as pd
from app.operations.base import Condition


class ColumnCondition(Condition):
    """Works over a columns"""
    def __init__(self, column: str, value: Any):
        self.column = column
        self.value = value
    
    def get_used_columns(self) -> set[str]:
        return {self.column}

# -- Comparison Filters --

class ComparisonCondition(ColumnCondition):
    SYMBOL = ""
    def __init__(self, column: str, value: Any):
        super().__init__(column, value)
    
    def to_code(self):
        return f"df['{self.column}'] {self.SYMBOL} {self.value}"

class EqualsCondition(ComparisonCondition):
    SYMBOL = "=="
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] == self.value


class NotEqualsCondition(ComparisonCondition):
    SYMBOL = "!="
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] != self.value


class GreaterThanCondition(ComparisonCondition):
    SYMBOL = ">"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] > self.value


class GreaterThanOrEqualsCondition(ComparisonCondition):
    SYMBOL = ">="
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] >= self.value


class LessThanCondition(ComparisonCondition):
    SYMBOL = "<"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] < self.value


class LessThanOrEqualsCondition(ComparisonCondition):
    SYMBOL = "<="
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] <= self.value


# -- Nullability Conditions --
class NullabilityCondition(ColumnCondition):
    METHOD =  ""
    def __init__(self, column, value = None):
        super().__init__(column, value)
    
    def to_code(self) -> str:
        return f"df['{self.column}'].{self.METHOD}()"

class BooleanIdentityCondition(ColumnCondition):
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].astype(bool)
    
    def to_code(self) -> str:
        return f"df['{self.column}']"

class IsNullCondition(NullabilityCondition):
    METHOD = "isnull"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].isnull()


class IsNotNullCondition(NullabilityCondition):
    METHOD = "notnull"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].notnull()


# -- String Filters --


class StringCondition(ColumnCondition):
    METHOD = ""
    def __init__(self, column: str, value: str):
        super().__init__(column=column, value=value)

    def __str__(self):
        return f"df['{self.column}'].str.{self.METHOD}('{self.value}')"

class ContainsCondition(StringCondition):
    METHOD = "contains"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].str.contains(self.value)


class DoesNotContainCondition(StringCondition):
    METHOD = "contains"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return ~df[self.column].str.contains(self.value)

    def __str__(self):
        return f"~df['{self.column}'].str.{self.METHOD}('{self.value}')"


class StartsWithCondition(StringCondition):
    METHOD = "startswith"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].str.startswith(self.value)


class EndsWithCondition(StringCondition):
    METHOD = "endswith"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].str.endswith(self.value)


# -- Membership Filters --

class MembershipCondition(ColumnCondition):
    NEGATION = ""
    def __init__(self, column: str, value: List[Any]):
        super().__init__(column, value)
    
    def to_code(self) -> str:
        return f"{self.NEGATION}df['{self.column}'].isin({self.value})"

class InCondition(MembershipCondition):
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].isin(self.value)

class NotInCondition(MembershipCondition):
    NEGATION = "~"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return ~df[self.column].isin(self.value)

# -- Logical Conditions --

class LogicalCondition(Condition):
    SYMBOL = ""
    def __init__(self, left: Condition, right: Condition):
        self.left = left
        self.right = right
    
    def to_code(self):
        left_str = f"({self.left})" if isinstance(self.left, LogicalCondition) else str(self.left)
        right_str = f"({self.right})" if isinstance(self.right, LogicalCondition) else str(self.right)
        
        return f"{left_str} {self.SYMBOL} {right_str}"
    
    def get_used_columns(self) -> set[str]:
        return self.left.get_used_columns().union(self.right.get_used_columns())

class AndCondition(LogicalCondition):
    SYMBOL = "&"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return self.left.apply(df) & self.right.apply(df)

class OrCondition(LogicalCondition):
    SYMBOL = "|"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return self.left.apply(df) | self.right.apply(df)

# -- Inverted Conditions --

class InvertCondition(LogicalCondition):
    SYMBOL = "~"
    def __init__(self, left: Condition, right: Condition = None):
        self.left = left
    
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return ~self.left.apply(df)
    
    def to_code(self):
        left_str = f"({self.left})" if isinstance(self.left, LogicalCondition) else str(self.left)
        return f"{self.SYMBOL} {left_str}"
    
    def get_used_columns(self) -> set[str]:
        return self.left.get_used_columns()

from app.operations.condition.base import ColumnCondition
import pandas as pd


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

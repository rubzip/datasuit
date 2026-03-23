from app.operations.condition.base import ColumnCondition
from app.core.constants import AcceptedTypes
import pandas as pd

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

import pandas as pd
from app.operations.condition.base import ColumnCondition


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

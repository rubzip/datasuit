from typing import List, Any
import pandas as pd
from app.operations.condition.base import ColumnCondition


class MembershipCondition(ColumnCondition):
    NEGATION = ""
    def __init__(self, column: str, value: List[Any]):
        super().__init__(column, value)
    
    def to_code(self) -> str:
        return f"{self.NEGATION}df['{self.column}'].isin({self.value})"

class InCondition(MembershipCondition):
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].isin(self.value)

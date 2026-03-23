from typing import Set, List
import pandas as pd
from app.operations.base import Operation, Condition


class FilterOperation(Operation):
    def __init__(self, condition: Condition):
        self.condition = condition

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[self.condition.apply(df)]

    def to_code(self) -> List[str]:
        return [f"mask = df[{self.condition.to_code()}]", f"df = df[mask]"]

    def get_used_columns(self) -> Set[str]:
        return self.condition.get_used_columns()

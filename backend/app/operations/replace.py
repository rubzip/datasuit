from typing import Set, List, Any
import pandas as pd
from app.operations.base import Operation

class ReplaceValueOperation(Operation):
    def __init__(self, column: str, old_value: Any, new_value: Any):
        self.column = column
        self.old_value = old_value
        self.new_value = new_value

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out[self.column] = out[self.column].replace(self.old_value, self.new_value)
        return out

    def to_code(self) -> List[str]:
        old_repr = f"'{self.old_value}'" if isinstance(self.old_value, str) else str(self.old_value)
        new_repr = f"'{self.new_value}'" if isinstance(self.new_value, str) else str(self.new_value)
        
        return [f"df['{self.column}'] = df['{self.column}'].replace({old_repr}, {new_repr})"]

    def get_used_columns(self) -> Set[str]:
        return {self.column}

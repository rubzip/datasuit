from typing import Set, List, Any
import pandas as pd
from app.operations.base import Operation

class InsertValueOperation(Operation):
    def __init__(self, column: str, value: Any):
        self.column = column
        self.value = value

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out[self.column] = self.value
        return out

    def to_code(self) -> List[str]:
        val_repr = f"'{self.value}'" if isinstance(self.value, str) else str(self.value)
        return [f"df['{self.column}'] = {val_repr}"]

    def get_used_columns(self) -> Set[str]:
        return set()

class InsertValueByIndexOperation(Operation):
    def __init__(self, index: Any, column: str, new_value: Any):
        self.index = index
        self.column = column
        self.new_value = new_value

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        if self.index in out.index:
            out.at[self.index, self.column] = self.new_value
        return out

    def to_code(self) -> List[str]:
        idx_repr = f"'{self.index}'" if isinstance(self.index, str) else str(self.index)
        new_repr = f"'{self.new_value}'" if isinstance(self.new_value, str) else str(self.new_value)
        
        return [f"df.at[{idx_repr}, '{self.column}'] = {new_repr}"]

    def get_used_columns(self) -> Set[str]:
        return {self.column}

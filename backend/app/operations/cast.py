from typing import Set, List
import pandas as pd
from app.operations.base import Operation
from app.core.constants import AcceptedTypes

class CastOperation(Operation):
    def __init__(self, column: str, to_type: AcceptedTypes):
        self.column = column
        self.to_type = to_type
    
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        if self.to_type == AcceptedTypes.NUMERIC:
            out[self.column] = pd.to_numeric(out[self.column], errors='coerce')
            return out
        if self.to_type == AcceptedTypes.DATETIME:
            out[self.column] = pd.to_datetime(out[self.column], errors='coerce')
            return out
        if self.to_type == AcceptedTypes.STRING:
            out[self.column] = out[self.column].astype(str)
            return out
        if self.to_type == AcceptedTypes.BOOLEAN:
            out[self.column] = out[self.column].astype(bool)
            return out
        raise ValueError(f"Unsupported type: {self.to_type}")

    def to_code(self) -> List[str]:
        if self.to_type == AcceptedTypes.NUMERIC:
            return [f"df['{self.column}'] = pd.to_numeric(df['{self.column}'], errors='coerce')"]
        if self.to_type == AcceptedTypes.DATETIME:
            return [f"df['{self.column}'] = pd.to_datetime(df['{self.column}'], errors='coerce')"]
        if self.to_type == AcceptedTypes.STRING:
            return [f"df['{self.column}'] = df['{self.column}'].astype(str)"]
        if self.to_type == AcceptedTypes.BOOLEAN:
            return [f"df['{self.column}'] = df['{self.column}'].astype(bool)"]
        raise ValueError(f"Unsupported type: {self.to_type}")

    def get_used_columns(self) -> Set[str]:
        return {self.column}

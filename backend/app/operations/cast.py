from typing import Set, List
import pandas as pd
from app.operations.base import Operation
from app.core.constants import AcceptedTypes


class CastOperation(Operation):
    def __init__(self, column: str, to_type: AcceptedTypes):
        self.column = column
        self.to_type = to_type

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def to_code(self) -> List[str]:
        # Simple mapping for now
        pd_type = "float" if self.to_type == AcceptedTypes.NUMERIC else "str"
        return [f"df['{self.column}'] = df['{self.column}'].astype('{pd_type}')"]

    def get_used_columns(self) -> Set[str]:
        return {self.column}

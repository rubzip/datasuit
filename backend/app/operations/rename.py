from typing import Set, List, Dict
import pandas as pd
from app.operations.base import Operation


class RenameColumnOperation(Operation):
    def __init__(self, column_mapping: Dict[str, str]):
        self.column_mapping = column_mapping

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns=self.column_mapping)

    def to_code(self) -> List[str]:
        if not self.column_mapping:
            return []
        return [f"df = df.rename(columns={self.column_mapping})"]

    def get_used_columns(self) -> Set[str]:
        return set(self.column_mapping.keys())

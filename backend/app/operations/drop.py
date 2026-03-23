from typing import List, Set
import pandas as pd
from app.operations.base import Operation


class BaseDropOperation(Operation):
    METHOD_NAME = ""

    def __init__(self, columns: List[str] = None):
        self.columns = columns

    def get_used_columns(self) -> Set[str]:
        if self.columns:
            return set(self.columns)
        return set()

    def to_code(self) -> List[str]:
        subset = f"subset={self.columns}" if self.columns else ""
        return [f"df = df.{self.METHOD_NAME}({subset})"]


class DropNAOperation(BaseDropOperation):
    METHOD_NAME = "dropna"

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.columns:
            return df.dropna(subset=self.columns)
        return df.dropna()


class DropDuplicatesOperation(BaseDropOperation):
    METHOD_NAME = "drop_duplicates"

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.columns:
            return df.drop_duplicates(subset=self.columns)
        return df.drop_duplicates()

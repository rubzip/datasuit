from typing import List, Set
import pandas as pd
from app.actions.base import Action


class BaseDrop(Action):
    METHOD_NAME = ""
    def __init__(self, columns: List[str] = None):
        self.columns = columns

    def get_used_columns(self) -> Set[str]:
        return set(self.columns)
    
    def to_code(self) -> List[str]:
        subset = f"subset={self.columns}" if self.columns else ""
        return [f"df = df.{self.METHOD_NAME}({subset})"]

class DropNARows(BaseDrop):
    METHOD_NAME = "dropna"
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.columns:
            return df.dropna(subset=self.columns)
        return df.dropna()

class DropDuplicates(BaseDrop):
    METHOD_NAME = "drop_duplicates"
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.columns:
            return df.drop_duplicates(subset=self.columns)
        return df.drop_duplicates()

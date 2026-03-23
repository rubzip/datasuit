from typing import List, Set
from backend.app.utils.base import BaseAction


class BaseDrop(BaseAction):
    def __init__(self, columns: List[str] = None):
        self.columns = columns

    def get_used_columns(self) -> Set[str]:
        return set(self.columns)

class DropNARows(BaseDrop):
    def apply(self, df: DataFrame) -> pd.DataFrame:
        if self.columns:
            return df.dropna(subset=self.columns)
        return df.dropna()

    def to_code(self) -> str:
        subset = f"subset={self.columns}" if self.columns else ""
        return f"df = df.dropna({subset})"

class DropDuplicates(BaseDrop):
    def apply(self, df: DataFrame) -> pd.DataFrame:
        if self.columns:
            return df.drop_duplicates(subset=self.columns)
        return df.drop_duplicates()

    def to_code(self) -> str:
        subset = f"subset={self.columns}" if self.columns else ""
        return f"df = df.drop_duplicates({subset})"

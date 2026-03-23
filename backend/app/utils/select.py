from typing import List, Set
import pandas as pd
from backend.app.utils.base import BaseAction


class SelectAction(BaseAction):
    def __init__(self, columns: List[str] = None):
        self.columns = columns

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.columns:
            return df[self.columns]
        return df

    def to_code(self) -> str:
        if self.columns:
            return f"df = df[{self.columns}]"
        return ""

    def get_used_columns(self) -> Set[str]:
        if self.columns:
            return {self.columns}
        return set()

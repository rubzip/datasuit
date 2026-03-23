from typing import List, Set
import pandas as pd
from backend.app.utils.base import BaseAction


class SelectAction(BaseAction):
    def __init__(self, columns: List[str] = None, limit: int = None):
        self.columns = columns
        self.limit = limit

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        if self.columns:
            out = out[self.columns]
        if self.limit:
            out = out.head()
        return out

    def to_code(self) -> str:
        lines = []
        if self.columns:
            return lines.append(f"df = df[{self.columns}]")
        if self.limit is not None:
            return lines.append(f"df = df.head({self.limit})")
        return '\n'.join(lines)

    def get_used_columns(self) -> Set[str]:
        if self.columns:
            return {self.columns}
        return set()

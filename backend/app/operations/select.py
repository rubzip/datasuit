from typing import List, Set
import pandas as pd
from app.operations.base import Operation


class SelectOperation(Operation):
    def __init__(
        self, columns: List[str] = None, limit: int = None, offset: int = None
    ):
        self.columns = columns
        self.limit = limit
        self.offset = offset

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        if self.columns:
            out = out[self.columns]

        if self.offset is not None:
            out = out.iloc[self.offset :]

        if self.limit is not None:
            out = out.head(self.limit)
        return out

    def to_code(self) -> List[str]:
        code = []
        if self.columns:
            code.append(f"df = df[{self.columns}]")

        if self.offset is not None:
            code.append(f"df = df.iloc[{self.offset}:]")

        if self.limit is not None:
            code.append(f"df = df.head({self.limit})")
        return code

    def get_used_columns(self) -> Set[str]:
        if self.columns:
            return set(self.columns)
        return set()

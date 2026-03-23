from typing import Set, List, Literal, Union
import pandas as pd
from app.operations.base import Operation


class SortOperation(Operation):
    def __init__(self, columns: List[str], ascending: List[bool], na_position: Literal["last", "first"] = "last"):
        self.columns = columns
        self.ascending = ascending
        self.na_position = na_position
        self.__validate_ascending()

    def __validate_ascending(self):
        if len(self.ascending) != len(self.columns):
            raise ValueError("Ascending must be a list of booleans with the same length as columns")

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.columns:
            return df
        return df.sort_values(by=self.columns, ascending=self.ascending, na_position=self.na_position)

    def to_code(self) -> List[str]:
        if not self.columns:
            return []
        return [f"df = df.sort_values(by={self.columns}, ascending={self.ascending}, na_position='{self.na_position}')"]

    def get_used_columns(self) -> Set[str]:
        if self.columns:
            return set(self.columns)
        return set()

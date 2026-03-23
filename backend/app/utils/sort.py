from typing import List
import pandas as pd
from app.schemas import OrderItem
from backend.app.utils.mask import BaseMask
import pandas as pd


class SortAction(BaseAction):
    def __init__(self, by: Optional[List[OrderItem]] = None, na_position=Literal["last"]):
        if not by:
            self.columns = []
            self.ascending = []
        self.columns = [item.column for item in by]
        self.ascending = [item.ascending for item in by]
        self.na_position = na_position

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.columns:
            return df
        return df.sort_values(by=columns, ascending=ascending, na_position='last')

    def to_code(self) -> str:
        if not self.columns:
            return ""
        return f"df = df.sort_values(by={self.columns}, ascending={self.ascending}, na_position='{self.na_position}')"

    def get_used_columns(self) -> Set[str]:
        if self.columns:
            return set(self.columns)
        return set()


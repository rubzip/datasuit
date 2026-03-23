from typing import Set
from app.utils.base import BaseAction
from app.utils.mask import Mask
import pandas as pd


class FilterAction(BaseAction):
    def __init__(self, mask: Mask):
        self.mask = mask

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[self.mask.apply(df)]

    def to_code(self) -> str:
        return f"df = df[{self.mask.to_code()}]"

    def get_used_columns(self) -> Set[str]:
        return self.mask.get_used_columns()

from typing import Set, List
import pandas as pd
from app.utils.base import Action
from app.utils.mask import Mask


class FilterAction(Action):
    def __init__(self, mask: Mask):
        self.mask = mask

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[self.mask.apply(df)]

    def to_code(self) -> List[str]:
        return [f"mask = df[{self.mask.to_code()}]", f"df = df[mask]"]

    def get_used_columns(self) -> Set[str]:
        return self.mask.get_used_columns()

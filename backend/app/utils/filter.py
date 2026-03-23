from backend.app.utils.mask import BaseMask
import pandas as pd


class FilterAction(BaseAction):
    def __init__(self, mask: BaseMask):
        self.mask = mask

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[self.mask.apply(df)]

    def to_code(self) -> str:
        return f"df = df[{self.mask.to_code()}]"

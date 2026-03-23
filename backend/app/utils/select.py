from backend.app.utils.mask import BaseMask
import pandas as pd


class SelectAction(BaseAction):
    def __init__(self, columns: List[str] = None):
        self.columns = columns

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        if columns:
            return df[self.columns]
        return df

    def to_code(self) -> str:
        if columns:
            return f"df = df[{self.columns}]"
        return ""

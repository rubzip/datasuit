from typing import List
import pandas as pd


def select_columns(df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
    if columns is None:
        return df
    return df[columns]
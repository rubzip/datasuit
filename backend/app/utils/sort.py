from typing import List
import pandas as pd
from app.schemas import OrderItem


def sort(df: pd.DataFrame, by: Optional[List[OrderItem]] = None):
    if not by:
        return

    columns = [item.column for item in by]
    ascending = [item.ascending for item in by]

    return df.sort_values(by=columns, ascending=ascending, na_position='last')

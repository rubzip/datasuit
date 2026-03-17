import pandas as pd
from app.schemas import Query


def get(df: pd.DataFrame, q: Query) -> pd.DataFrame:
    out = df.copy()
    
    if q.where:
        pass
    if q.dropna:
        pass
    if q.drop_duplicates:
        pass
    if q.limit:
        pass
    if q.offset:
        pass
    if q.select:
        pass

    return out

def get_code(df: pd.DataFrame, q: Query) -> List[str]:
    out = []
    
    if q.where:
        pass
    if q.dropna:
        pass
    if q.drop_duplicates:
        pass
    if q.limit:
        pass
    if q.offset:
        pass
    if q.select:
        pass

    return out

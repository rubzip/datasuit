def drop_na(df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
    if columns is None:
        return df.dropna()
    return df.dropna(subset=columns)

def drop_duplicates(df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
    if columns is None:
        return df.drop_duplicates()
    return df.drop_duplicates(subset=columns)

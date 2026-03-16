from typing import List
import pandas as pd
from schemas import Query, FilterCondition, FilterOperator

def select(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    return df[columns]

def dropna(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    if columns:
        return df.dropna(subset=columns)
    return df.dropna()

def drop_duplicates(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    if columns:
        return df.drop_duplicates(subset=columns)
    return df.drop_duplicates()

def where(df: pd.DataFrame, filter: FilterCondition) -> pd.DataFrame:
    if filter.operator == FilterOperator.EQUAL:
        return df[df[filter.column] == filter.value]
    elif filter.operator == FilterOperator.NOT_EQUAL:
        return df[df[filter.column] != filter.value]

def order_by(df: pd.DataFrame, order_by: OrderItem) -> pd.DataFrame:
    return df.sort_values(by=order_by.column, ascending=order_by.ascending)


def engine(df: pd.DataFrame, query: Query) -> pd.DataFrame:
    if query.dropna:
        df = dropna(df, query.columns.columns)
    if query.drop_duplicates:
        df = drop_duplicates(df, query.columns.columns)
    if query.filters:
        df = where(df, query.filters)
    if query.order_by:
        df = order_by(df, query.order_by)
    if query.limit:
        df = df.head(query.limit)
    if query.offset:
        df = df.iloc[query.offset:]
    if query.columns:
        df = select(df, query.columns.columns)
    return df

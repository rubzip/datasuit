from typing import List
import pandas as pd


def validate_column(df: pd.DataFrame, column: str):
    cols = df.columns
    if column not in cols:
        raise ValueError(f"Column {column} not found in DataFrame")


def validate_multiple_columns(df: pd.DataFrame, columns: List[str]):
    cols = df.columns
    for col in columns:
        if col not in cols:
            raise ValueError(f"Column {col} not found in DataFrame")


def validate_str(value: str):
    if not isinstance(value, str):
        raise ValueError(f"Value {value} is not a string")


def validate_is_list(value: List[str]):
    if not isinstance(value, list):
        raise ValueError(f"Value {value} is not a list")

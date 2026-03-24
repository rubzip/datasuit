import pandas as pd
import io
from typing import BinaryIO


def __force_types(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors="coerce")
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = pd.to_datetime(df[col], errors="coerce")
        elif pd.api.types.is_bool_dtype(df[col]):
            df[col] = df[col].astype(bool)
        else:
            df[col] = df[col].astype(str)
    return df


def load_csv(file: BinaryIO) -> pd.DataFrame:
    """Load CSV from a binary file-like object (e.g., FastAPI UploadFile.file)"""
    return __force_types(pd.read_csv(file))


def load_json(file: BinaryIO) -> pd.DataFrame:
    """Load JSON from a binary file-like object"""
    return __force_types(pd.read_json(file))


def load_excel(file: BinaryIO) -> pd.DataFrame:
    """Load Excel from a binary file-like object"""
    return __force_types(pd.read_excel(file))


def load_from_binary(file: BinaryIO, format: str) -> pd.DataFrame:
    """Load DataFrame from a binary file-like object and format string."""
    fmt = format.lower()
    if fmt == "csv" or "csv" in fmt:
        return load_csv(file)
    if fmt == "json" or "json" in fmt:
        return load_json(file)
    if fmt == "excel" or "xlsx" in fmt or "xls" in fmt:
        return load_excel(file)
    raise ValueError(f"Unsupported binary format: {format}")

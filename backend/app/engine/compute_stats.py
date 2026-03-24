import pandas as pd
from app.schemas.api.responses import ColumnStats, DataHealthReportResponse


def get_stats(series: pd.Series) -> ColumnStats:
    count = int(series.count())
    null_count = int(series.isnull().sum())
    distinct_count = int(series.nunique())

    is_numeric = pd.api.types.is_numeric_dtype(series)
    is_datetime = pd.api.types.is_datetime64_any_dtype(series)
    is_bool = pd.api.types.is_bool_dtype(series)
    is_string = pd.api.types.is_string_dtype(series)

    # Cast metrics to float/int to avoid numpy types in Pydantic
    mean = float(series.mean()) if is_numeric else None
    
    # Allow min/max for numeric, datetime and strings (alphabetical)
    min_val = None
    max_val = None
    if is_numeric or is_datetime or is_string:
        try:
            min_val = series.min()
            max_val = series.max()
        except:
            pass

    # Min/Max handling for non-numeric might need more care depending on what Any allows
    if min_val is not None and not isinstance(min_val, (int, float, str, bool)):
        min_val = str(min_val)
    if max_val is not None and not isinstance(max_val, (int, float, str, bool)):
        max_val = str(max_val)

    return ColumnStats(
        count=count,
        null_count=null_count,
        distinct_count=distinct_count,
        mean=mean,
        min=min_val,
        max=max_val,
    )


def compute_health_report(df: pd.DataFrame) -> DataHealthReportResponse:
    columns_stats = {}
    for col in df.columns:
        columns_stats[col] = get_stats(df[col])
    
    return DataHealthReportResponse(
        total_rows=len(df),
        total_columns=len(df.columns),
        memory_usage=str(df.memory_usage(deep=True).sum()),
        columns=columns_stats
    )

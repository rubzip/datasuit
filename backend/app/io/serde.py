import pandas as pd
from typing import Any, Dict, List, Optional
from app.schemas.api.responses import DatasetPreviewResponse, Row
from app.schemas.base import TypedValue
from app.core.constants import AcceptedTypes
from app.engine.compute_stats import compute_health_report


def __get_accepted_type(dtype: Any) -> AcceptedTypes:
    if pd.api.types.is_numeric_dtype(dtype):
        return AcceptedTypes.NUMERIC
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return AcceptedTypes.DATETIME
    if pd.api.types.is_bool_dtype(dtype):
        return AcceptedTypes.BOOLEAN
    return AcceptedTypes.STRING


def to_dataset_preview(df: pd.DataFrame, sample_size: int = 100, include_health: bool = True) -> DatasetPreviewResponse:
    """
    Serializes a DataFrame to the DatasetPreviewResponse format.
    Includes columns-oriented data and column types.
    """
    preview_df = df.head(sample_size)
    
    # Column orientation (current state)
    data = preview_df.to_dict(orient="list")
    
    # Row orientation (with TypedValue for every cell - very detailed but heavier)
    rows = []
    for idx, row_series in preview_df.iterrows():
        row_values = {}
        for col in preview_df.columns:
            val = row_series[col]
            # Convert numpy types to native Python types for Pydantic
            if pd.api.types.is_number(val):
                if pd.api.types.is_integer(val):
                    val = int(val)
                else:
                    val = float(val) if not pd.isna(val) else None
            elif isinstance(val, bool):
                val = bool(val)
            elif pd.isna(val):
                val = None
            else:
                val = str(val)

            row_values[col] = TypedValue(
                type=__get_accepted_type(type(val)),
                value=val
            )
        rows.append(Row(
            index=TypedValue(type=__get_accepted_type(type(idx)), value=idx),
            values=row_values
        ))
    
    # Extract types
    types = {col: __get_accepted_type(preview_df[col].dtype) for col in preview_df.columns}
    
    # Compute health if requested
    health = compute_health_report(df) if include_health else None
    
    return DatasetPreviewResponse(
        data=data,
        rows=rows,
        types=types,
        health=health
    )

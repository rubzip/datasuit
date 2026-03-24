from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from app.core.constants import AcceptedTypes
from app.schemas.base import TypedValue


class ColumnStats(BaseModel):
    count: int
    null_count: int
    distinct_count: int
    mean: Optional[float] = None
    min: Optional[Any] = None
    max: Optional[Any] = None


class DataHealthReportResponse(BaseModel):
    total_rows: int
    total_columns: int
    memory_usage: str
    columns: Dict[str, ColumnStats]

class Row(BaseModel):
    index: TypedValue
    values: Dict[str, str]


class DatasetPreviewResponse(BaseModel):
    data: Dict[str, List[Any]] # Column-oriented (Efficient)
    rows: List[Row] = [] # Row-oriented (Typed, but heavy)
    types: Dict[str, AcceptedTypes]
    health: Optional[DataHealthReportResponse] = None

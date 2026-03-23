from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from app.core.constants import AcceptedTypes

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

class DatasetPreviewResponse(BaseModel):
    data: Dict[str, List[Any]]
    types: Dict[str, AcceptedTypes]
    health: Optional[DataHealthReportResponse] = None

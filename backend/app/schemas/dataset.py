from typing import List, Optional, Any, Dict
from pydantic import BaseModel


class DatasetResponse(BaseModel):
    data: Dict[str, List[Any]]
    types: Dict[str, AcceptedTypes]

class ColumnStats(BaseModel):
    count: int
    null_count: int
    distinct_count: int
    mean: Optional[float] = None
    min: Optional[Any] = None
    max: Optional[Any] = None

class DataHealthReport(BaseModel):
    total_rows: int
    total_columns: int
    memory_usage: str
    columns: Dict[str, ColumnStats]

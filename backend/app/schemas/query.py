from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from app.core.constants import AcceptedTypes
from app.schemas.filter import FilterCondition, ComposedFilterCondition, Union


class OrderItem(BaseModel):
    column: str
    ascending: bool = True


class Query(BaseModel):
    select: List[str] = []
    where: Optional[Union[FilterCondition, ComposedFilterCondition]] = None
    order_by: Optional[List[OrderItem]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    dropna: Optional[bool] = False
    drop_duplicates: Optional[bool] = False


class Transform(BaseModel):
    pass


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


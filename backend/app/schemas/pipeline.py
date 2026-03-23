from typing import List, Optional
from pydantic import BaseModel
from app.schemas.base import OrderItem
from app.schemas.conditions import ConditionType

class PipelineConfig(BaseModel):
    select_columns: Optional[List[str]] = None
    condition: Optional[ConditionType] = None
    order_by: Optional[List[OrderItem]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    
    dropna: bool = False
    drop_duplicates: bool = False

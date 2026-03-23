from typing import List, Optional
from pydantic import BaseModel
from app.schemas.base import OrderItem
from app.schemas.conditions import ConditionTypeSchema


class PipelineConfig(BaseModel):
    select: Optional[List[str]] = None
    where: Optional[ConditionTypeSchema] = None
    order_by: Optional[List[OrderItem]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None

    dropna: bool = False
    drop_duplicates: bool = False

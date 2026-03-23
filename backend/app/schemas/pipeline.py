from typing import List, Optional, Dict
from pydantic import BaseModel
from app.schemas.base import OrderItem, ReplaceConfig, InsertConfig
from app.schemas.conditions import ConditionTypeSchema
from app.core.constants import AcceptedTypes


class PipelineConfig(BaseModel):
    select: Optional[List[str]] = None
    where: Optional[ConditionTypeSchema] = None
    order_by: Optional[List[OrderItem]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None

    dropna: bool = False
    drop_duplicates: bool = False

    rename: Optional[Dict[str, str]] = None
    replace: Optional[List[ReplaceConfig]] = None
    insert: Optional[List[InsertConfig]] = None
    cast: Optional[Dict[str, AcceptedTypes]] = None

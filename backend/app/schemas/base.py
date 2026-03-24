from typing import Optional, Literal, List, Any
from pydantic import BaseModel
from app.core.constants import AcceptedTypes


class TypedValue(BaseModel):
    type: AcceptedTypes
    value: Any


class TypedList(BaseModel):
    type: AcceptedTypes
    value: List[Any]


class OrderItem(BaseModel):
    column: str
    ascending: bool = True
    na_position: Literal["first", "last"] = "last"


class ReplaceConfig(BaseModel):
    column: str
    old_value: TypedValue
    new_value: TypedValue


class InsertConfig(BaseModel):
    column: str
    value: TypedValue
    index: Optional[TypedValue] = None

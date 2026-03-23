from typing import Any, Literal, List
from pydantic import BaseModel
from app.core.constants import AcceptedTypes


class TypedValue(BaseModel):
    type: AcceptedTypes
    value: str


class TypedList(BaseModel):
    type: AcceptedTypes
    value: List[str]


class OrderItem(BaseModel):
    column: str
    ascending: bool = True
    na_position: Literal["first", "last"] = "last"

from typing import List, Optional, Any, Union, Set, Dict, Callable
from enum import Enum

import pandas as pd
from pydantic import BaseModel

from app.core.constants import AcceptedTypes, FilterOperator, CompositionOperator


### --- Where --- ###


class TypedValue(BaseModel):
    type: AcceptedTypes
    value: str


class FilterCondition(BaseModel):
    column: str
    operator: FilterOperator
    value: Optional[TypedValue] = None


class ComposedFilterCondition(BaseModel):
    left_condition: Union[FilterCondition, "ComposedFilterCondition"]
    operator: CompositionOperator
    right_condition: Optional[Union[FilterCondition, "ComposedFilterCondition"]] = None


ComposedFilterCondition.model_rebuild()


def get_columns(condition: Union[FilterCondition, ComposedFilterCondition, None]) -> Set[str]:
    if condition is None:
        return set()
    if isinstance(condition, FilterCondition):
        return {condition.column}
    if isinstance(condition, ComposedFilterCondition):
        cols = get_columns(condition.left_condition)
        if self.right_condition:
            cols = cols.union(get_columns(right_condition))
        return cols
    raise 


# -- Order By ---

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

from enum import Enum
from typing import Callable, Dict, List, Optional, Set, Union
from pydantic import BaseModel


class TypeList(Enum):
    STRING = "string"
    NUMERIC = "numeric"
    BOOLEAN = "boolean"
    DATE = "date"


class FilterOperator(Enum):
    EQUAL = "eq"
    NOT_EQUAL = "ne"





### --- Select --- ###

class Select(BaseModel):
    columns: List[str]


### --- Where --- ###


class TypedValue(BaseModel):
    type: TypeList
    value: str


class FilterCondition(BaseModel):
    column: str
    operator: FilterOperator
    value: Optional[TypedValue] = None


class ComposedFilterCondition(BaseModel):
    left_condition: Union[FilterCondition, ComposedFilterCondition]
    operator: FilterOperator
    right_condition: Union[FilterCondition, ComposedFilterCondition]


# -- Order By ---

class OrderItem(BaseModel):
    column: str
    ascending: bool = True


class Query(BaseModel):
    columns: Select # SELECT
    filters: Optional[Union[FilterCondition, ComposedFilterCondition]] = None # WHERE
    order_by: Optional[OrderItem] = None # ORDER BY
    dropna: Optional[bool] = False
    drop_duplicates: Optional[bool] = False

from typing import List, Optional, Any, Union, Set
from pydantic import BaseModel
from app.core.constants import AcceptedTypes, FilterOperator, CompositionOperator


class TypedValue(BaseModel):
    type: AcceptedTypes
    value: str


class Filter(BaseModel):
    operator: Union[FilterOperator, CompositionOperator]


class FilterCondition(Filter):
    column: str
    operator: FilterOperator
    value: Optional[TypedValue] = None # Maybe should exist the possibility of list fro IN operator
    values: Optional[List[TypedValue]] = None # For IN operator


class ComposedFilterCondition(Filter):
    left_condition: Union[FilterCondition, "ComposedFilterCondition"]
    operator: CompositionOperator
    right_condition: Optional[Union[FilterCondition, "ComposedFilterCondition"]] = None


ComposedFilterCondition.model_rebuild()

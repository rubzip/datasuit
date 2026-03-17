from typing import List, Optional, Any, Union, Set
from pydantic import BaseModel
from app.core.constants import AcceptedTypes, FilterOperator, CompositionOperator


class TypedValue(BaseModel):
    type: AcceptedTypes
    value: str


class FilterCondition(BaseModel):
    column: str
    operator: FilterOperator
    value: Optional[TypedValue] = None

    def get_columns(self) -> Set[str]:
        return {self.column}


class ComposedFilterCondition(BaseModel):
    left_condition: Union[FilterCondition, "ComposedFilterCondition"]
    operator: CompositionOperator
    right_condition: Optional[Union[FilterCondition, "ComposedFilterCondition"]] = None

    def get_columns(self) -> Set[str]:
        cols = self.left_condition.get_columns()
        if self.right_condition:
            cols = cols.union(self.right_condition.get_columns())
        return cols


ComposedFilterCondition.model_rebuild()


def get_columns(condition: Union[FilterCondition, ComposedFilterCondition, None]) -> Set[str]:
    if condition is None:
        return set()
    if isinstance(condition, FilterCondition):
        return {condition.column}
    if isinstance(condition, ComposedFilterCondition):
        cols = get_columns(condition.left_condition)
        if condition.right_condition:
            cols = cols.union(get_columns(condition.right_condition))
        return cols
    raise ValueError(f"Unsupported condition type: {type(condition)}")

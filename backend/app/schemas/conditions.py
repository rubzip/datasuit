from typing import List, Optional, Union, Literal
from pydantic import BaseModel, Field
from app.core.constants import FilterOperator, CompositionOperator, OperatorType
from app.schemas.base import TypedValue, TypedList


class BaseCondition(BaseModel):
    operator: OperatorType

class BaseSingleCondition(BaseModel):
    column: str

class ComparisonCondition(BaseSingleCondition):
    operator: Literal[
        FilterOperator.EQUAL, 
        FilterOperator.NOT_EQUAL,
        FilterOperator.GREATER,
        FilterOperator.LESS,
        FilterOperator.CONTAINS,
        FilterOperator.STARTSWITH,
        FilterOperator.ENDSWITH,
        FilterOperator.IS_NULL,
        FilterOperator.IS_NOT_NULL,
        FilterOperator.IS_IN,
        FilterOperator.IS_NOT_IN
    ]
    value: TypedValue

class NullCheckCondition(BaseSingleCondition):
    operator: Literal[
        FilterOperator.IS_NULL, 
        FilterOperator.IS_NOT_NULL,
    ]

class MembershipCondition(BaseSingleCondition):
    operator: Literal[
        FilterOperator.IS_IN, 
        FilterOperator.IS_NOT_IN
    ]
    values: TypedList

SingleCondition = Union[
    ComparisonCondition, 
    NullCheckCondition, 
    MembershipCondition
]

class CompositeCondition(BaseCondition):
    left_condition: Union[SingleCondition, "CompositeCondition"]
    operator: CompositionOperator
    right_condition: Optional[Union[SingleCondition, "CompositeCondition"]] = None

CompositeCondition.model_rebuild()

ConditionType = Union[SingleCondition, CompositeCondition]

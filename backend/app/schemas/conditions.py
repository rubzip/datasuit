from typing import List, Optional, Union, Literal
from pydantic import BaseModel, Field
from app.core.constants import FilterOperator, CompositionOperator, OperatorType
from app.schemas.base import TypedValue, TypedList


class BaseConditionSchema(BaseModel):
    operator: OperatorType

class BaseSingleConditionSchema(BaseModel):
    column: str

class ComparisonConditionSchema(BaseSingleConditionSchema):
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

class NullCheckConditionSchema(BaseSingleConditionSchema):
    operator: Literal[
        FilterOperator.IS_NULL, 
        FilterOperator.IS_NOT_NULL,
    ]

class MembershipConditionSchema(BaseSingleConditionSchema):
    operator: Literal[
        FilterOperator.IS_IN, 
        FilterOperator.IS_NOT_IN
    ]
    values: TypedList

SingleConditionSchema = Union[
    ComparisonConditionSchema, 
    NullCheckConditionSchema, 
    MembershipConditionSchema
]

class CompositeConditionSchema(BaseConditionSchema):
    left_condition: Union[SingleConditionSchema, "CompositeConditionSchema"]
    operator: CompositionOperator
    right_condition: Optional[Union[SingleConditionSchema, "CompositeConditionSchema"]] = None

CompositeConditionSchema.model_rebuild()

ConditionTypeSchema = Union[SingleConditionSchema, CompositeConditionSchema]

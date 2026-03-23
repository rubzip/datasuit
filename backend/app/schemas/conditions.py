from typing import Optional, Union
from pydantic import BaseModel, model_validator
from app.core.constants import FilterOperator, CompositionOperator
from app.schemas.base import TypedValue, TypedList


class SingleConditionSchema(BaseModel):
    column: str
    operator: FilterOperator
    value: Optional[TypedValue] = None
    values: Optional[TypedList] = None

    @model_validator(mode="after")
    def validate_operator_values(self):
        # Reglas simples y legibles:
        null_ops = [
            FilterOperator.IS_NULL,
            FilterOperator.IS_NOT_NULL,
            FilterOperator.IDENTITY,
        ]
        list_ops = [FilterOperator.IS_IN, FilterOperator.IS_NOT_IN]

        if self.operator in null_ops:
            if self.value or self.values:
                raise ValueError(f"Operator {self.operator} doesn't take values.")
        elif self.operator in list_ops:
            if not self.values:
                raise ValueError(
                    f"Operator {self.operator} requires 'values' (a list)."
                )
        else:
            if not self.value:
                raise ValueError(f"Operator {self.operator} requires 'value'.")

        return self


class CompositeConditionSchema(BaseModel):
    left_condition: Union[SingleConditionSchema, "CompositeConditionSchema"]
    operator: CompositionOperator
    right_condition: Optional[
        Union[SingleConditionSchema, "CompositeConditionSchema"]
    ] = None


CompositeConditionSchema.model_rebuild()

ConditionTypeSchema = Union[SingleConditionSchema, CompositeConditionSchema]

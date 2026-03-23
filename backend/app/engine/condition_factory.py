from typing import Dict, Union
from app.operations.base import Condition
from app.operations.conditions import (
    ColumnCondition,
    LogicalCondition,
    EqualsCondition,
    NotEqualsCondition,
    GreaterThanCondition,
    GreaterThanOrEqualsCondition,
    LessThanCondition,
    LessThanOrEqualsCondition,
    IsNullCondition,
    IsNotNullCondition,
    IdentityCondition,
    ContainsCondition,
    StartsWithCondition,
    EndsWithCondition,
    InCondition,
    AndCondition,
    OrCondition,
    NotCondition,
)

from app.core.constants import FilterOperator, CompositionOperator
from app.schemas.conditions import (
    ConditionTypeSchema,
    CompositeConditionSchema,
    SingleConditionSchema,
)
from app.engine.cast_type import cast_typed_value, cast_typed_list


class ConditionFactory:
    MAPPER_CONDITION: Dict[FilterOperator, type[ColumnCondition]] = {
        FilterOperator.EQUAL: EqualsCondition,
        FilterOperator.NOT_EQUAL: NotEqualsCondition,
        FilterOperator.GREATER: GreaterThanCondition,
        FilterOperator.GREATER_EQUAL: GreaterThanOrEqualsCondition,
        FilterOperator.LESS: LessThanCondition,
        FilterOperator.LESS_EQUAL: LessThanOrEqualsCondition,
        FilterOperator.IS_NULL: IsNullCondition,
        FilterOperator.IS_NOT_NULL: IsNotNullCondition,
        FilterOperator.CONTAINS: ContainsCondition,
        FilterOperator.STARTSWITH: StartsWithCondition,
        FilterOperator.ENDSWITH: EndsWithCondition,
        FilterOperator.IDENTITY: IdentityCondition,
        FilterOperator.IS_IN: InCondition,
    }

    MAPPER_COMPOSITION: Dict[CompositionOperator, type[LogicalCondition]] = {
        CompositionOperator.AND: AndCondition,
        CompositionOperator.OR: OrCondition,
        CompositionOperator.NOT: NotCondition,
    }

    @classmethod
    def build_condition(cls, schema: ConditionTypeSchema) -> Condition:
        if isinstance(schema, CompositeConditionSchema):
            left = cls.build_condition(schema.left_condition)
            right = (
                cls.build_condition(schema.right_condition)
                if schema.right_condition
                else None
            )
            op_class = cls.MAPPER_COMPOSITION[schema.operator]
            return op_class(left=left, right=right)

        if isinstance(schema, SingleConditionSchema):
            op_class = cls.MAPPER_CONDITION[schema.operator]

            if schema.value:
                real_val = cast_typed_value(schema.value)
                return op_class(column=schema.column, value=real_val)
            elif schema.values:
                real_list = cast_typed_list(schema.values)
                return op_class(column=schema.column, value=real_list)
            else:
                return op_class(column=schema.column)

    @classmethod
    def get_condition_class(cls, operator: FilterOperator) -> type[Condition]:
        op_class = cls.MAPPER_CONDITION.get(operator)
        if not op_class:
            raise ValueError(f"Unknown filter operator: {operator}")
        return op_class

    @classmethod
    def get_composition_class(cls, operator: CompositionOperator) -> type[Condition]:
        op_class = cls.MAPPER_COMPOSITION.get(operator)
        if not op_class:
            raise ValueError(f"Unknown composition operator: {operator}")
        return op_class

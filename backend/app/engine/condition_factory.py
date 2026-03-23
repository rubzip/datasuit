from typing import Dict, List, Union
from app.operations.base import Condition
from app.operations.condition import ColumnCondition, LogicalCondition
from app.operations.condition import (
    EqualsCondition, NotEqualsCondition, GreaterThanCondition, GreaterThanOrEqualsCondition, LessThanCondition, LessThanOrEqualsCondition,
    IsNullCondition, IsNotNullCondition, ContainsCondition, DoesNotContainCondition, StartsWithCondition,
    EndsWithCondition, InCondition, NotInCondition, BooleanIdentityCondition,
    AndCondition, OrCondition, InvertCondition
)
from app.core.constants import FilterOperator, CompositionOperator
from app.schemas.conditions import SingleCondition, CompositeCondition, ConditionType



MAPPER_CONDITION: Dict[FilterOperator, ColumnCondition] = {
    FilterOperator.EQUAL: EqualsCondition,
    FilterOperator.NOT_EQUAL: NotEqualsCondition,
    FilterOperator.GREATER: GreaterThanCondition,
    FilterOperator.GREATER_EQUAL: GreaterThanOrEqualsCondition,
    FilterOperator.LESS: LessThanCondition,
    FilterOperator.LESS_EQUAL: LessThanOrEqualsCondition,
    FilterOperator.IS_NULL: IsNullCondition,
    FilterOperator.IS_NOT_NULL: IsNotNullCondition,
    FilterOperator.CONTAINS: ContainsCondition,
    FilterOperator.NOT_CONTAINS: DoesNotContainCondition,
    FilterOperator.STARTSWITH: StartsWithCondition,
    FilterOperator.ENDSWITH: EndsWithCondition,
    FilterOperator.IS_IN: InCondition,
    FilterOperator.IS_NOT_IN: NotInCondition,
    FilterOperator.IDENTITY: BooleanIdentityCondition,
}

MAPPER_COMPOSITION: Dict[CompositionOperator, LogicalCondition] = {
    CompositionOperator.AND: AndCondition,
    CompositionOperator.OR: OrCondition,
    CompositionOperator.NOT: InvertCondition,
}


def condition_factory(condition: ConditionType) -> Condition:
    if isinstance(condition, SingleCondition):
        return MAPPER_CONDITION.get(condition.operator)(
            column=condition.column,
            value=condition.value
        )
    if isinstance(condition, CompositeCondition):
        return MAPPER_COMPOSITION.get(condition.operator)(
            left=condition_factory(condition.left_condition),
            right=condition_factory(condition.right_condition)
        )
    raise ValueError(f"Invalid filter operator: {condition}")

from typing import Dict, List, Union
from app.actions.base import Mask
from app.actions.mask import ColumnMask, BinaryMask
from app.actions.mask import (
    EqualMask, NotEqualMask, GreaterMask, GreaterEqualMask, LessMask, LessEqualMask,
    IsNullMask, IsNotNullMask, ContainsMask, NotContainsMask, StartsWithMask,
    EndsWithMask, IsInMask, IsNotInMask, IdentityMask,
    AndMask, OrMask, NotMask
)
from app.core.constants import FilterOperator, CompositionOperator
from app.schemas.filter import FilterCondition, ComposedFilterCondition

MAPPER_MASK: Dict[FilterOperator, ColumnMask] = {
    FilterOperator.EQUAL: EqualMask,
    FilterOperator.NOT_EQUAL: NotEqualMask,
    FilterOperator.GREATER: GreaterMask,
    FilterOperator.GREATER_EQUAL: GreaterEqualMask,
    FilterOperator.LESS: LessMask,
    FilterOperator.LESS_EQUAL: LessEqualMask,
    FilterOperator.IS_NULL: IsNullMask,
    FilterOperator.IS_NOT_NULL: IsNotNullMask,
    FilterOperator.CONTAINS: ContainsMask,
    FilterOperator.NOT_CONTAINS: NotContainsMask,
    FilterOperator.STARTSWITH: StartsWithMask,
    FilterOperator.ENDSWITH: EndsWithMask,
    FilterOperator.IS_IN: IsInMask,
    FilterOperator.IS_NOT_IN: IsNotInMask,
    FilterOperator.IDENTITY: IdentityMask,
}

MAPPER_COMPOSITION: Dict[CompositionOperator, BinaryMask] = {
    CompositionOperator.AND: AndMask,
    CompositionOperator.OR: OrMask,
    CompositionOperator.NOT: NotMask,
}


def mask_factory(filter: Union[FilterCondition, ComposedFilterCondition]) -> Mask:
    if isinstance(filter, ComposedFilterCondition):
        return MAPPER_COMPOSITION.get(filter.operator)(
            left=mask_factory(filter.left_condition),
            right=mask_factory(filter.right_condition)
        )
    if isinstance(filter, FilterCondition):
        return MAPPER_MASK.get(filter.operator)(
            column=filter.column,
            value=filter.value
        )
    raise ValueError(f"Invalid filter operator: {filter}")

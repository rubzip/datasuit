from typing import Dict
from app.operations.base import Condition
from app.operations.condition.base import ColumnCondition, LogicalCondition
from app.operations.condition.comparison import (
    EqualsCondition, NotEqualsCondition, GreaterThanCondition, GreaterThanOrEqualsCondition, LessThanCondition, LessThanOrEqualsCondition
)
from app.operations.condition.null import IsNullCondition, IsNotNullCondition, BooleanIdentityCondition
from app.operations.condition.string import ContainsCondition, StartsWithCondition, EndsWithCondition
from app.operations.condition.membership import InCondition
from app.operations.condition.logical import AndCondition, OrCondition, NotCondition

from app.core.constants import FilterOperator, CompositionOperator
from app.schemas.conditions import (
    ConditionTypeSchema, ComparisonConditionSchema, NullCheckConditionSchema, 
    MembershipConditionSchema, CompositeConditionSchema
)
from app.engine.cast_type import cast_typed_value, cast_typed_list

# Mapas de diccionarios (igual que los tenías)
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
        FilterOperator.IDENTITY: BooleanIdentityCondition,
    }

    MAPPER_COMPOSITION: Dict[CompositionOperator, type[LogicalCondition]] = {
        CompositionOperator.AND: AndCondition,
        CompositionOperator.OR: OrCondition,
        CompositionOperator.NOT: NotCondition,
    }

    @classmethod
    def condition_factory(cls, condition: ConditionTypeSchema) -> Condition:
        """
        Convierte un Schema Pydantic validado en una Operación ejecutable de Pandas.
        """
        if isinstance(condition, CompositeConditionSchema):
            left_node = cls.condition_factory(condition.left_condition)
            right_node = cls.condition_factory(condition.right_condition) if condition.right_condition else None
            
            op_class = cls.get_composition_class(condition)
            return op_class(left=left_node, right=right_node)

        op_class = cls.get_condition_class(condition)
        if isinstance(condition, ComparisonConditionSchema):
            real_value = cast_typed_value(condition.value)
            return op_class(column=condition.column, value=real_value)

        if isinstance(condition, NullCheckConditionSchema):
            return op_class(column=condition.column)

        if isinstance(condition, MembershipConditionSchema):
            real_list = cast_typed_list(condition.values)
            return op_class(column=condition.column, value=real_list)

        raise ValueError(f"Unknown condition type: {type(condition)}")
    
    @classmethod
    def build_condition(cls, condition: ConditionTypeSchema) -> Condition:
        return cls.condition_factory(condition)
    
    @classmethod
    def get_condition_class(cls, condition: ConditionTypeSchema) -> type[Condition]:
        op_class = cls.MAPPER_CONDITION.get(condition.operator)
        if not op_class:
            raise ValueError(f"Unknown composition operator: {condition.operator}")
        return op_class

    @classmethod
    def get_composition_class(cls, condition: ConditionTypeSchema) -> type[Condition]:
        op_class = cls.MAPPER_COMPOSITION.get(condition.operator)
        if not op_class:
            raise ValueError(f"Unknown composition operator: {condition.operator}")
        return op_class

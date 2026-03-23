import pytest
from app.engine.condition_factory import ConditionFactory
from app.schemas.conditions import SingleConditionSchema, CompositeConditionSchema
from app.schemas.base import TypedValue
from app.core.constants import FilterOperator, CompositionOperator, AcceptedTypes
from app.operations.conditions import EqualsCondition, AndCondition

def test_build_single_condition():
    schema = SingleConditionSchema(
        column="age",
        operator=FilterOperator.EQUAL,
        value=TypedValue(type=AcceptedTypes.NUMERIC, value="30")
    )
    cond = ConditionFactory.build_condition(schema)
    assert isinstance(cond, EqualsCondition)
    assert cond.column == "age"
    assert cond.value == 30.0

def test_build_composite_condition():
    s1 = SingleConditionSchema(
        column="age",
        operator=FilterOperator.EQUAL,
        value=TypedValue(type=AcceptedTypes.NUMERIC, value="30")
    )
    s2 = SingleConditionSchema(
        column="city",
        operator=FilterOperator.EQUAL,
        value=TypedValue(type=AcceptedTypes.STRING, value="NY")
    )
    schema = CompositeConditionSchema(
        left_condition=s1,
        operator=CompositionOperator.AND,
        right_condition=s2
    )
    cond = ConditionFactory.build_condition(schema)
    assert isinstance(cond, AndCondition)
    assert isinstance(cond.left, EqualsCondition)
    assert isinstance(cond.right, EqualsCondition)

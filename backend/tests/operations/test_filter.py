import pytest
import pandas as pd
from app.operations.filter import FilterOperation
from app.operations.conditions import EqualsCondition

def test_filter_operation_apply(sample_df):
    cond = EqualsCondition(column='active', value=True)
    op = FilterOperation(condition=cond)
    result = op.apply(sample_df)
    assert len(result) == 3
    assert all(result['active'])

def test_filter_operation_to_code():
    cond = EqualsCondition(column='active', value=True)
    op = FilterOperation(condition=cond)
    code = op.to_code()
    assert len(code) == 2
    assert "mask = df[" in code[0]
    assert "df[mask]" in code[1]

def test_filter_operation_used_columns():
    cond = EqualsCondition(column='active', value=True)
    op = FilterOperation(condition=cond)
    assert op.get_used_columns() == {'active'}

import pytest
import pandas as pd
from app.operations.cast import CastOperation
from app.core.constants import AcceptedTypes

def test_cast_operation_apply(sample_df):
    # Dummy implementation for now as CastOperation.apply is 'pass'
    op = CastOperation(column='age', to_type=AcceptedTypes.NUMERIC)
    result = op.apply(sample_df)
    assert result is None # Currently returns nothing or passes

def test_cast_operation_to_code():
    op = CastOperation(column='age', to_type=AcceptedTypes.NUMERIC)
    code = op.to_code()
    assert len(code) == 1
    assert "astype" in code[0]
    assert "float" in code[0]

def test_cast_operation_used_columns():
    op = CastOperation(column='age', to_type=AcceptedTypes.NUMERIC)
    assert op.get_used_columns() == {'age'}

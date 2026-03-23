import pytest
import pandas as pd
import numpy as np
from app.operations.cast import CastOperation
from app.core.constants import AcceptedTypes

def test_cast_operation_numeric():
    df = pd.DataFrame({"a": ["1", "2.5", "invalid", None]})
    op = CastOperation(column="a", to_type=AcceptedTypes.NUMERIC)
    result = op.apply(df)
    
    assert pd.api.types.is_numeric_dtype(result["a"])
    assert result["a"].iloc[0] == 1.0
    assert result["a"].iloc[1] == 2.5
    assert np.isnan(result["a"].iloc[2])

def test_cast_operation_datetime():
    df = pd.DataFrame({"a": ["2023-01-01", "2023-02-01", "invalid"]})
    op = CastOperation(column="a", to_type=AcceptedTypes.DATETIME)
    result = op.apply(df)
    
    assert pd.api.types.is_datetime64_any_dtype(result["a"])
    assert result["a"].iloc[0] == pd.Timestamp("2023-01-01")
    assert pd.isna(result["a"].iloc[2])

def test_cast_operation_string():
    df = pd.DataFrame({"a": [1, 2.5, True]})
    op = CastOperation(column="a", to_type=AcceptedTypes.STRING)
    result = op.apply(df)
    
    assert result["a"].dtype == object or pd.api.types.is_string_dtype(result["a"])
    assert result["a"].iloc[0] == "1"
    assert result["a"].iloc[1] == "2.5"
    assert result["a"].iloc[2] == "True"

def test_cast_operation_boolean():
    df = pd.DataFrame({"a": [1, 0, "", "hello", None]})
    op = CastOperation(column="a", to_type=AcceptedTypes.BOOLEAN)
    result = op.apply(df)
    
    assert result["a"].dtype == bool
    assert result["a"].iloc[0] == True
    assert result["a"].iloc[1] == False
    assert result["a"].iloc[4] == False # Pandas bool(None) is False

def test_cast_operation_to_code():
    op = CastOperation(column="age", to_type=AcceptedTypes.NUMERIC)
    code = op.to_code()
    assert len(code) == 1
    assert "pd.to_numeric" in code[0]
    assert "'age'" in code[0]

def test_cast_operation_used_columns():
    op = CastOperation(column="age", to_type=AcceptedTypes.NUMERIC)
    assert op.get_used_columns() == {"age"}

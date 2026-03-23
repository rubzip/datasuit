import pytest
import pandas as pd
from app.engine.cast_type import cast_typed_value, cast_typed_list
from app.schemas.base import TypedValue, TypedList
from app.core.constants import AcceptedTypes

def test_cast_typed_value():
    assert cast_typed_value(TypedValue(type=AcceptedTypes.NUMERIC, value="10.5")) == 10.5
    assert cast_typed_value(TypedValue(type=AcceptedTypes.BOOLEAN, value="True")) == True
    assert cast_typed_value(TypedValue(type=AcceptedTypes.STRING, value="hello")) == "hello"
    ts = cast_typed_value(TypedValue(type=AcceptedTypes.DATETIME, value="2023-01-01"))
    assert isinstance(ts, pd.Timestamp)

def test_cast_typed_list():
    val = TypedList(type=AcceptedTypes.NUMERIC, value=["1", "2.5", "3"])
    assert cast_typed_list(val) == [1.0, 2.5, 3.0]
    
    val2 = TypedList(type=AcceptedTypes.STRING, value=["a", "b"])
    assert cast_typed_list(val2) == ["a", "b"]

def test_cast_error():
    with pytest.raises(TypeError):
        cast_typed_value(TypedValue(type=AcceptedTypes.NUMERIC, value="not_a_number"))

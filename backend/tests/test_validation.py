import pytest
import pandas as pd
from app.validation import validate_column, validate_multiple_columns, validate_str, validate_is_list

def test_validate_column():
    df = pd.DataFrame({'a': [1], 'b': [2]})
    validate_column(df, 'a')
    with pytest.raises(ValueError, match="not found"):
        validate_column(df, 'c')

def test_validate_multiple_columns():
    df = pd.DataFrame({'a': [1], 'b': [2]})
    validate_multiple_columns(df, ['a', 'b'])
    with pytest.raises(ValueError, match="not found"):
        validate_multiple_columns(df, ['a', 'c'])

def test_validate_types():
    validate_str("hello")
    with pytest.raises(ValueError, match="not a string"):
        validate_str(123)
    
    validate_is_list(["a", "b"])
    with pytest.raises(ValueError, match="not a list"):
        validate_is_list("not a list")

import pytest
import pandas as pd
from app.operations.select import SelectOperation

def test_select_apply(sample_df):
    op = SelectOperation(columns=['name', 'age'], limit=2, offset=1)
    result = op.apply(sample_df)
    assert len(result) == 2
    assert list(result.columns) == ['name', 'age']
    assert result['name'].tolist() == ['Bob', 'Charlie']

def test_select_to_code():
    op = SelectOperation(columns=['name'], limit=5, offset=10)
    code = op.to_code()
    assert len(code) == 3
    assert "df[['name']]" in code[0]
    assert "iloc[10:]" in code[1]
    assert "head(5)" in code[2]

def test_select_used_columns():
    op = SelectOperation(columns=['a', 'b'])
    assert op.get_used_columns() == {'a', 'b'}

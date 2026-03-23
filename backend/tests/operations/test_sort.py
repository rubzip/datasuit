import pytest
import pandas as pd
from app.operations.sort import SortOperation

def test_sort_apply(sample_df):
    op = SortOperation(columns=['salary'], ascending=[False])
    result = op.apply(sample_df)
    assert result['salary'].iloc[0] == 90000
    assert result['name'].iloc[0] == 'Eve'

def test_sort_to_code():
    op = SortOperation(columns=['a', 'b'], ascending=[True, False], na_position='first')
    code = op.to_code()
    assert len(code) == 1
    assert "sort_values" in code[0]
    assert "ascending=[True, False]" in code[0]
    assert "na_position='first'" in code[0]

def test_sort_used_columns():
    op = SortOperation(columns=['col1'], ascending=[True])
    assert op.get_used_columns() == {'col1'}

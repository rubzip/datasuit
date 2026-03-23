import pytest
import pandas as pd
from app.operations.insert import InsertValueOperation, InsertValueByIndexOperation

def test_insert_value_operation_apply(sample_df):
    op = InsertValueOperation(column="new_col", value=42)
    result = op.apply(sample_df)
    
    assert "new_col" in result.columns
    assert (result["new_col"] == 42).all()
    # Ensure original is not modified
    assert "new_col" not in sample_df.columns

def test_insert_value_operation_to_code():
    op = InsertValueOperation(column="new_col", value="hello")
    code = op.to_code()
    assert len(code) == 1
    assert "df['new_col'] = 'hello'" in code[0]

def test_insert_value_by_index_operation_apply(sample_df):
    # sample_df has 3 rows with indices 0, 1, 2
    op = InsertValueByIndexOperation(index=1, column="age", new_value=99)
    result = op.apply(sample_df)
    
    assert result.at[1, "age"] == 99
    assert result.at[0, "age"] != 99 # unchanged

def test_insert_value_by_index_operation_to_code():
    op = InsertValueByIndexOperation(index="row1", column="age", new_value=99)
    code = op.to_code()
    assert len(code) == 1
    assert "df.at['row1', 'age'] = 99" in code[0]

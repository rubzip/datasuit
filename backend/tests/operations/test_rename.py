import pytest
import pandas as pd
from app.operations.rename import RenameColumnOperation

def test_rename_column_operation_apply(sample_df):
    mapping = {"name": "full_name", "age": "years"}
    op = RenameColumnOperation(column_mapping=mapping)
    result = op.apply(sample_df)
    
    assert "full_name" in result.columns
    assert "years" in result.columns
    assert "name" not in result.columns
    assert "age" not in result.columns

def test_rename_column_operation_to_code():
    mapping = {"name": "full_name"}
    op = RenameColumnOperation(column_mapping=mapping)
    code = op.to_code()
    assert len(code) == 1
    assert "df.rename(columns={'name': 'full_name'})" in code[0]

def test_rename_column_operation_used_columns():
    mapping = {"name": "full_name", "age": "years"}
    op = RenameColumnOperation(column_mapping=mapping)
    assert op.get_used_columns() == {"name", "age"}

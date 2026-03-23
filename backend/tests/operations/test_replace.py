import pytest
import pandas as pd
from app.operations.replace import ReplaceValueOperation

def test_replace_value_operation_apply(sample_df):
    # sample_df "name" has ["Alice", "Bob", "Charlie"]
    op = ReplaceValueOperation(column="name", old_value="Bob", new_value="Robert")
    result = op.apply(sample_df)
    
    assert result["name"].iloc[1] == "Robert"
    assert result["name"].iloc[0] == "Alice" # unchanged

def test_replace_value_operation_to_code():
    op = ReplaceValueOperation(column="name", old_value="Bob", new_value="Robert")
    code = op.to_code()
    assert len(code) == 1
    assert "df['name'].replace('Bob', 'Robert')" in code[0]

def test_replace_value_operation_used_columns():
    op = ReplaceValueOperation(column="name", old_value="Bob", new_value="Robert")
    assert op.get_used_columns() == {"name"}

import pytest
import pandas as pd
from app.operations.drop import DropNAOperation, DropDuplicatesOperation

def test_dropna_apply(sample_df):
    op = DropNAOperation(columns=['age'])
    result = op.apply(sample_df)
    assert len(result) == 4
    assert not result['age'].isnull().any()

def test_dropna_to_code():
    op = DropNAOperation(columns=['age'])
    code = op.to_code()
    assert len(code) == 1
    assert "dropna" in code[0]
    assert "subset=['age']" in code[0]

def test_drop_duplicates_apply():
    df = pd.DataFrame({'a': [1, 1, 2], 'b': [3, 3, 4]})
    op = DropDuplicatesOperation()
    result = op.apply(df)
    assert len(result) == 2

def test_drop_duplicates_to_code():
    op = DropDuplicatesOperation(columns=['a'])
    code = op.to_code()
    assert len(code) == 1
    assert "drop_duplicates" in code[0]
    assert "subset=['a']" in code[0]

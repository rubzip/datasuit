import pytest
import pandas as pd
from app.io.load import load_csv, load_json, load_from_binary

def test_load_csv_binary(sample_df, df_to_binary):
    binary_data = df_to_binary(sample_df, format="csv")
    loaded_df = load_csv(binary_data)
    
    # We expect some type forcing (e.g. strings for 'name')
    assert loaded_df["name"].iloc[0] == "Alice"
    assert loaded_df["age"].iloc[0] == 25.0
    assert len(loaded_df) == 5

def test_load_json_binary(sample_df, df_to_binary):
    binary_data = df_to_binary(sample_df, format="json")
    loaded_df = load_json(binary_data)
    
    assert loaded_df["name"].iloc[0] == "Alice"
    assert len(loaded_df) == 5

def test_load_from_binary_dispatcher(sample_df, df_to_binary):
    # Test CSV dispatch
    csv_data = df_to_binary(sample_df, format="csv")
    loaded_csv = load_from_binary(csv_data, "csv")
    assert len(loaded_csv) == 5
    
    # Test JSON dispatch
    json_data = df_to_binary(sample_df, format="json")
    loaded_json = load_from_binary(json_data, "application/json")
    assert len(loaded_json) == 5

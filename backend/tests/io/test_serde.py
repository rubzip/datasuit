import pytest
import pandas as pd
from app.io.serde import to_dataset_preview

def test_to_dataset_preview(sample_df):
    response = to_dataset_preview(sample_df, sample_size=2)
    
    # Check column-oriented data
    assert "name" in response.data
    assert response.data["name"] == ["Alice", "Bob"]
    
    # Check row-oriented data
    assert len(response.rows) == 2
    assert response.rows[0].values["name"].value == "Alice"
    assert response.rows[0].values["name"].type.value == "string"
    
    # Check types
    assert response.types["age"].value == "numeric"
    
    # Check health
    assert response.health is not None
    assert response.health.total_rows == 5

import pytest
import pandas as pd
from app.engine.compute_stats import get_stats, compute_health_report

def test_get_stats_numeric():
    series = pd.Series([10, 20, 30, None])
    stats = get_stats(series)
    
    assert stats.count == 3
    assert stats.null_count == 1
    assert stats.distinct_count == 3
    assert stats.mean == 20.0
    assert stats.min == 10.0
    assert stats.max == 30.0

def test_get_stats_string():
    series = pd.Series(["a", "b", "a", None])
    stats = get_stats(series)
    
    assert stats.count == 3
    assert stats.null_count == 1
    assert stats.distinct_count == 2
    assert stats.mean is None
    assert stats.min == "a"
    assert stats.max == "b"

def test_compute_health_report(sample_df):
    report = compute_health_report(sample_df)
    
    assert report.total_rows == 5
    assert report.total_columns == 5
    assert "name" in report.columns
    assert "age" in report.columns
    assert report.columns["age"].null_count == 1

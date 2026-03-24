import pytest
import pandas as pd
import io
from app.schemas.pipeline import PipelineConfig
from app.schemas.base import OrderItem


@pytest.fixture
def sample_df():
    data = {
        "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "age": [25, 30, 35, 40, None],
        "city": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
        "salary": [50000, 60000, 70000, 80000, 90000],
        "active": [True, False, True, False, True],
    }
    return pd.DataFrame(data)


@pytest.fixture
def empty_pipeline_config():
    return PipelineConfig()


@pytest.fixture
def df_to_binary():
    def _convert(df: pd.DataFrame, format: str = "csv"):
        output = io.BytesIO()
        if format == "csv":
            df.to_csv(output, index=False)
        elif format == "json":
            df.to_json(output, orient="records")
        output.seek(0)
        return output

    return _convert

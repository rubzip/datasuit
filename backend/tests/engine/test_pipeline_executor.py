import pytest
import pandas as pd
from app.engine.pipeline_executor import PipelineExecutor
from app.schemas.pipeline import PipelineConfig
from app.schemas.conditions import SingleConditionSchema
from app.schemas.base import OrderItem
from app.core.constants import FilterOperator

def test_pipeline_complex_execution(sample_df):
    # Pipeline:
    # 1. dropna
    # 2. filter age > 25
    # 3. sort by salary desc
    # 4. limit 2
    # 5. select name, salary
    
    config = PipelineConfig(
        dropna=True,
        where=SingleConditionSchema(
            column='age',
            operator=FilterOperator.GREATER,
            value={'type': 'numeric', 'value': '25'}
        ),
        order_by=[OrderItem(column='salary', ascending=False)],
        limit=2,
        select=['name', 'salary']
    )
    
    executor = PipelineExecutor(config)
    result = executor.apply(sample_df)
    
    # After dropna: Alice(25), Bob(30), Charlie(35), David(40) (Eve dropped)
    # After filter age > 25: Bob(30), Charlie(35), David(40)
    # After sort salary desc: David(80k), Charlie(70k), Bob(60k)
    # After limit 2: David, Charlie
    # After select: ['name', 'salary']
    
    assert len(result) == 2
    assert result['name'].tolist() == ['David', 'Charlie']
    assert list(result.columns) == ['name', 'salary']

def test_executor_empty_pipeline(sample_df):
    executor = PipelineExecutor(PipelineConfig())
    result = executor.apply(sample_df)
    pd.testing.assert_frame_equal(result, sample_df)

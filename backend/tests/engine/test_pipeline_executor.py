import pytest
import pandas as pd
from app.engine.pipeline_executor import PipelineExecutor
from app.schemas.pipeline import PipelineConfig
from app.schemas.conditions import SingleConditionSchema
from app.core.constants import FilterOperator, AcceptedTypes
from app.schemas.base import OrderItem, ReplaceConfig, InsertConfig

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

def test_pipeline_new_operations(sample_df):
    # Pipeline:
    # 1. Cast age to string
    # 2. Replace 'Alice' with 'Alicia' in name
    # 3. Insert 'country' column with 'Spain'
    # 4. Rename 'salary' to 'wage'
    
    config = PipelineConfig(
        cast={'age': AcceptedTypes.STRING},
        replace=[ReplaceConfig(
            column='name', 
            old_value={'type': AcceptedTypes.STRING, 'value': 'Alice'}, 
            new_value={'type': AcceptedTypes.STRING, 'value': 'Alicia'}
        )],
        insert=[InsertConfig(
            column='country', 
            value={'type': AcceptedTypes.STRING, 'value': 'Spain'}
        )],
        rename={'salary': 'wage'}
    )
    
    executor = PipelineExecutor(config)
    result = executor.apply(sample_df)
    
    # Assertions
    assert result['age'].dtype == object or pd.api.types.is_string_dtype(result['age'])
    assert result['name'].iloc[0] == 'Alicia'
    assert (result['country'] == 'Spain').all()
    assert 'wage' in result.columns
    assert 'salary' not in result.columns

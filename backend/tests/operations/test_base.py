import pytest
from app.operations.base import Operation

class MockOperation(Operation):
    def apply(self, df): return df
    def to_code(self): return ["df = test"]
    def get_used_columns(self): return set()

def test_base_component_str():
    op = MockOperation()
    assert str(op) == "df = test"

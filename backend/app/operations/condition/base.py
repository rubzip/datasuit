from typing import List, Any, Dict, Type
import pandas as pd
from app.core.constants import AcceptedTypes
from app.operations.base import Condition


class ColumnCondition(Condition):
    """Works over a columns"""
    def __init__(self, column: str, value: Any):
        self.column = column
        self.value = value
    
    def get_used_columns(self) -> set[str]:
        return {self.column}

class LogicalCondition(Condition):
    SYMBOL = ""
    def __init__(self, left: Condition, right: Condition):
        self.left = left
        self.right = right
    
    def to_code(self):
        left_str = f"({self.left})" if isinstance(self.left, LogicalCondition) else str(self.left)
        right_str = f"({self.right})" if isinstance(self.right, LogicalCondition) else str(self.right)
        
        return f"{left_str} {self.SYMBOL} {right_str}"
    
    def get_used_columns(self) -> set[str]:
        return self.left.get_used_columns().union(self.right.get_used_columns())

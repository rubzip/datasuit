from app.operations.condition.base import LogicalCondition
from app.operations.condition.base import Condition


class AndCondition(LogicalCondition):
    SYMBOL = "&"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return self.left.apply(df) & self.right.apply(df)

class OrCondition(LogicalCondition):
    SYMBOL = "|"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return self.left.apply(df) | self.right.apply(df)


class NotCondition(LogicalCondition):
    SYMBOL = "~"
    def __init__(self, left: Condition, right: Condition = None):
        self.left = left
    
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return ~self.left.apply(df)
    
    def to_code(self):
        left_str = f"({self.left})" if isinstance(self.left, LogicalCondition) else str(self.left)
        return f"{self.SYMBOL} {left_str}"
    
    def get_used_columns(self) -> set[str]:
        return self.left.get_used_columns()

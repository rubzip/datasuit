from typing import Set
import pandas as pd
from app.operations.base import Operation
from app.core.constants import AcceptedTypes


class CastOperation(Operation):
    def __init__(self, column: str, to_type: AcceptedTypes):
        self.column = column
        self.to_type = to_type
    
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def to_code(self) -> str:
        pass

    def get_used_columns(self) -> Set[str]:
        return {self.column}

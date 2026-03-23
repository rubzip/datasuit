from abc import ABC, abstractmethod
from typing import Any, List, Set
import pandas as pd
from app.utils.base import BaseAction
from app.core.constants import AcceptedTypes


class CastAction(BaseAction):
    def __init__(self, column: str, to_type: AcceptedTypes):
        self.column = column
        self.to_type = to_type
    
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def to_code(self) -> str:
        pass

    def get_used_columns(self) -> Set[str]:
        return {self.column}

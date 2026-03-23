from abc import ABC, abstractmethod
from typing import Any, List, Set
import pandas as pd


class BaseAction(ABC):
    """
    Abstract class for DataFrame transformations. Contains logic and code transforamtion.
    """
    
    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies logic to DataFrame."""
        pass

    @abstractmethod
    def to_code(self) -> List[str]:
        """Returns pandas code for specific transformation."""
        pass

    @abstractmethod
    def get_used_columns(self) -> Set[str]:
        pass

    def __str__(self):
        return '\n'.join(self.to_code())

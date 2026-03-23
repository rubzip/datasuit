from abc import ABC, abstractmethod
import pandas as pd
from typing import Any, List

class BaseAction(ABC):
    """
    Abstract class for DataFrame transformations. Contains logic and code transforamtion.
    """
    
    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies logic to DataFrame."""
        pass

    @abstractmethod
    def to_code(self) -> str:
        """Returns pandas code for specific transformation."""
        pass

    def __str__(self):
        return self.to_code()

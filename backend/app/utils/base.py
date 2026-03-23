from abc import ABC, abstractmethod
from typing import List, Set
import pandas as pd


class BaseComponent(ABC):
    """
    Abstract class for DataFrame transformations. Contains logic and code transforamtion.
    """

    @abstractmethod
    def to_code(self) -> List[str]:
        """Returns pandas code for specific transformation."""
        pass

    @abstractmethod
    def get_used_columns(self) -> Set[str]:
        """Returns all used columns."""
        pass

    def __str__(self):
        return '\n'.join(self.to_code())


class Action(BaseComponent):
    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies logic to DataFrame."""
        pass


class Mask(BaseComponent):
    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        """Applies logic to DataFrame."""
        pass

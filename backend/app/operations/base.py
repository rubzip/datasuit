from abc import ABC, abstractmethod
from typing import List, Set
import pandas as pd


class BaseComponent(ABC):
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
        """Returns all used columns."""
        pass

    def __str__(self):
        code = self.to_code()
        if isinstance(code, str):
            return code
        return "\n".join(code)


class Operation(BaseComponent):
    pass


class Condition(BaseComponent):
    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.Series:
        """Applies logic to DataFrame."""
        pass

    @abstractmethod
    def to_code(self) -> str:
        """Returns pandas code for the condition as a string."""
        pass

    def __str__(self):
        return self.to_code()

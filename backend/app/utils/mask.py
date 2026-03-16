from typing import List, Any
import pandas as pd
from app.constants import AcceptedTypes

class BaseMask:
    SYMBOL = ""

    def __init__(self, column: str, value: Any):
        self.column = column
        self.value = value

    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        raise NotImplementedError
    
    def __str__(self):
        return f"df['{self.column}'] {self.SYMBOL} {self.value}"
    

# -- Comparison Filters --


class MaskIdentity(BaseMask):
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].astype(bool)
    
    def __str__(self):
        return f"df['{self.column}'].astype(bool)"

class EqualMask(BaseMask):
    SYMBOL = "=="
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] == self.value


class NotEqualMask(BaseMask):
    SYMBOL = "!="
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] != self.value


class GreaterMask(BaseMask):
    SYMBOL = ">"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] > self.value


class GreaterEqualMask(BaseMask):
    SYMBOL = ">="
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] >= self.value


class LessMask(BaseMask):
    SYMBOL = "<"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] < self.value


class LessEqualMask(BaseMask):
    SYMBOL = "<="
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column] <= self.value


# -- Null Filters --


class NoValueMask(BaseMask):
    METHOD = ""
    def __init__(self, column: str, value: Any = None):
        self.column = column
    
    def __str__(self):
        return f"df['{self.column}'].{self.METHOD}()"


class MaskIsNull(NoValueMask):
    METHOD = "isnull"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].isnull()


class MaskIsNotNull(NoValueMask):
    METHOD = "notnull"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].notnull()


# -- String Filters --


class StringMask(BaseMask):
    METHOD = ""
    def __init__(self, column: str, value: str):
        self.column = column
        self.value = value
    
    def __str__(self):
        return f"df['{self.column}'].str.{self.METHOD}('{self.value}')"


class MaskContains(StringMask):
    METHOD = "contains"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].str.contains(self.value)


class MaskNotContains(StringMask):
    METHOD = "contains"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return ~df[self.column].str.contains(self.value)

    def __str__(self):
        return f"~df['{self.column}'].str.{self.METHOD}('{self.value}')"


class MaskStartsWith(StringMask):
    METHOD = "startswith"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].str.startswith(self.value)


class MaskEndsWith(StringMask):
    METHOD = "endswith"
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].str.endswith(self.value)


# -- Boolean Filters --


class MaskNot(BaseMask):
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return ~df[self.column].astype(bool)
    
    def __str__(self):
        return f"~df['{self.column}'].astype(bool)"


# -- Membership Filters --

class MembershipMask(BaseMask):
    def __init__(self, column: str, value: List[Any]):
        self.column = column
        self.value = value
    

class MaskIsIn(MembershipMask):
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return df[self.column].isin(self.value)
    
    def __str__(self):
        return f"df['{self.column}'].isin({self.value})"


class MaskIsNotIn(MembershipMask):
    def apply(self, df: pd.DataFrame) -> pd.Series[bool]:
        return ~df[self.column].isin(self.value)
    
    def __str__(self):
        return f"~df['{self.column}'].isin({self.value})"

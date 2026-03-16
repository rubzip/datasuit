import pandas as pd


def _compose_identity(left_mask: pd.Series[bool], right_mask: pd.Series[bool] = None) -> pd.Series[bool]:
    return left_mask

def _compose_and(left_mask: pd.Series[bool], right_mask: pd.Series[bool]) -> pd.Series[bool]:
    return left_mask & right_mask

def _compose_or(left_mask: pd.Series[bool], right_mask: pd.Series[bool]) -> pd.Series[bool]:
    return left_mask | right_mask

def _compose_not(left_mask: pd.Series[bool], right_mask: pd.Series[bool] = None) -> pd.Series[bool]:
    return ~left_mask

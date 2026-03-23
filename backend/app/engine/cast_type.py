from typing import Union, List
import pandas as pd
from app.core.constants import AcceptedTypes
from app.schemas.base import TypedValue, TypedList


def cast_typed_value(typed_value: TypedValue) -> Union[float, bool, str, pd.Timestamp]:
    try:
        if typed_value.type == AcceptedTypes.NUMERIC:
            return float(typed_value.value)
        if typed_value.type == AcceptedTypes.BOOLEAN:
            return bool(typed_value.value)
        if typed_value.type == AcceptedTypes.STRING:
            return str(typed_value.value)
        if typed_value.type == AcceptedTypes.DATETIME:
            return pd.to_datetime(typed_value.value)
        raise ValueError(f"Unsupported type: {typed_value.type}")
    except Exception as e:
        raise TypeError(f"Error casting value {typed_value.value} to type {typed_value.type}: {e}")

def cast_typed_list(typed_list: TypedList) -> List[Union[float, bool, str, pd.Timestamp]]:
    try:
        if typed_list.type == AcceptedTypes.NUMERIC:
            return [float(v) for v in typed_list.value]
        if typed_list.type == AcceptedTypes.BOOLEAN:
            return [bool(v) for v in typed_list.value]
        if typed_list.type == AcceptedTypes.STRING:
            return [str(v) for v in typed_list.value]
        if typed_list.type == AcceptedTypes.DATETIME:
            return [pd.to_datetime(v) for v in typed_list.value]
        raise ValueError(f"Unsupported type: {typed_list.type}")
    except Exception as e:
        raise TypeError(f"Error casting value {typed_list.value} to type {typed_list.type}: {e}")

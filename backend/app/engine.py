from typing import Set, List
import pandas as pd
from app.schemas import Query
from app.utils.select import SelectAction
from app.utils.filter import FilterAction
from app.utils.drop import DropNARows, DropDuplicates
from app.utils.mask import get_mask
from app.utils.base import BaseAction


class QueryEngine:
    def __init__(self, q: Query):
        self.pipeline: List[BaseAction] = self._build_pipeline()

    def _build_pipeline(self) -> List[BaseAction]:
        actions = []
        
        if self.query.dropna:
            actions.append(DropNARows())
        if self.query.drop_duplicates:
            actions.append(DropDuplicates())
            
        if self.query.where:
            mask = get_mask(self.query.where)
            actions.append(FilterAction(mask))
            
        if self.query.select or self.query.limit is not None or self.query.offset is not None:
            actions.append(SelectAction(
                columns=self.query.select, 
                limit=self.query.limit, 
                offset=self.query.offset
            ))
            
        return actions

    def validate(self, df: pd.DataFrame):
        used_cols = self.get_used_columns()
        missing = used_cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        for action in self.pipeline:
            out = action.apply(out)
        return out
    
    def get_used_columns(self) -> Set[str]:
        used_columns = set()
        for action in self.pipeline:
            used_columns.update(action.get_used_columns())
        return used_columns
    
    def get_code(self) -> List[str]:
        return [a.to_code() for a in self.pipeline]

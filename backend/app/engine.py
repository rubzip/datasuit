from typing import Set, List
import pandas as pd
from app.schemas import Query
from app.utils.select import SelectAction
from app.utils.filter import FilterAction
from app.utils.drop import DropNARows, DropDuplicates
from app.utils.mask import get_mask
from app.utils.base import Action


class QueryEngine:
    def __init__(self, q: Query):
        self.pipeline: List[Action] = self._build_pipeline(q)

    def _build_pipeline(self, q: Query) -> List[Action]:
        actions = []
        
        if q.dropna:
            actions.append(DropNARows())
        if q.drop_duplicates:
            actions.append(DropDuplicates())
            
        if q.where:
            mask = get_mask(q.where)
            actions.append(FilterAction(mask))
            
        if q.select or q.limit is not None or q.offset is not None:
            actions.append(SelectAction(
                columns=q.select, 
                limit=q.limit, 
                offset=q.offset
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
        return [c for a in self.pipeline for c in a.to_code()]

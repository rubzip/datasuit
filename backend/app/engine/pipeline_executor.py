from typing import Set, List
import pandas as pd
from app.schemas.pipeline import PipelineConfig
from app.operations.select import SelectOperation
from app.operations.filter import FilterOperation
from app.operations.sort import SortOperation
from app.operations.drop import DropNAOperation, DropDuplicatesOperation
from app.engine.condition_factory import ConditionFactory
from app.operations.base import Operation


class PipelineExecutor:
    """Query executor"""

    def __init__(self, pipeline: PipelineConfig):
        self.pipeline: List[Operation] = self._build_pipeline(pipeline)

    def _build_pipeline(self, pipeline: PipelineConfig) -> List[Operation]:
        operations = []

        if pipeline.dropna:
            operations.append(DropNAOperation())
        if pipeline.drop_duplicates:
            operations.append(DropDuplicatesOperation())

        if pipeline.where:
            condition = ConditionFactory.build_condition(pipeline.where)
            operations.append(FilterOperation(condition))

        if pipeline.order_by:
            columns = [c.column for c in pipeline.order_by]
            ascending = [c.ascending for c in pipeline.order_by]
            na_position = pipeline.order_by[0].na_position
            operations.append(SortOperation(columns, ascending, na_position))

        if pipeline.select or pipeline.limit is not None or pipeline.offset is not None:
            operations.append(
                SelectOperation(
                    columns=pipeline.select,
                    limit=pipeline.limit,
                    offset=pipeline.offset,
                )
            )

        return operations

    def validate(self, df: pd.DataFrame):
        used_cols = self.get_used_columns()
        missing = used_cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        self.validate(df)
        out = df.copy()
        for operation in self.pipeline:
            out = operation.apply(out)
        return out

    def get_used_columns(self) -> Set[str]:
        used_columns = set()
        for operation in self.pipeline:
            used_columns.update(operation.get_used_columns())
        return used_columns

    def get_code(self) -> List[str]:
        return [c for a in self.pipeline for c in a.to_code()]

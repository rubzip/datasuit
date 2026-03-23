from typing import Set, List
import pandas as pd
from app.schemas.pipeline import PipelineConfig
from app.operations.select import SelectOperation
from app.operations.filter import FilterOperation
from app.operations.sort import SortOperation
from app.operations.drop import DropNAOperation, DropDuplicatesOperation
from app.operations.cast import CastOperation
from app.operations.replace import ReplaceValueOperation
from app.operations.insert import InsertValueOperation, InsertValueByIndexOperation
from app.operations.rename import RenameColumnOperation
from app.engine.condition_factory import ConditionFactory
from app.engine.cast_type import cast_typed_value
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

        if pipeline.cast:
            for col, to_type in pipeline.cast.items():
                operations.append(CastOperation(col, to_type))

        if pipeline.replace:
            for r in pipeline.replace:
                old_val = cast_typed_value(r.old_value)
                new_val = cast_typed_value(r.new_value)
                operations.append(ReplaceValueOperation(r.column, old_val, new_val))

        if pipeline.insert:
            for i in pipeline.insert:
                val = cast_typed_value(i.value)
                if i.index is not None:
                    idx = cast_typed_value(i.index)
                    operations.append(InsertValueByIndexOperation(idx, i.column, val))
                else:
                    operations.append(InsertValueOperation(i.column, val))

        if pipeline.rename:
            operations.append(RenameColumnOperation(pipeline.rename))

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

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        for operation in self.pipeline:
            operation.validate(out)
            out = operation.apply(out)
        return out

    def get_used_columns(self) -> Set[str]:
        used_columns = set()
        for operation in self.pipeline:
            used_columns.update(operation.get_used_columns())
        return used_columns

    def get_code(self) -> List[str]:
        return [c for a in self.pipeline for c in a.to_code()]

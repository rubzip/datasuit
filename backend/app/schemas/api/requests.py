from pydantic import BaseModel
from app.schemas.pipeline import PipelineConfig

class ApplyPipelineRequest(BaseModel):
    dataset_id: str
    pipeline: PipelineConfig

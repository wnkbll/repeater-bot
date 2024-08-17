from datetime import datetime

from pydantic import BaseModel, Field


class IDModelMixin(BaseModel):
    id: int = Field(0, alias="id")


class TimestampsModelMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

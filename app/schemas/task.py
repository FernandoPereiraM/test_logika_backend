from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: int = Field(default=0, ge=0, le=2)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: int) -> int:
        if v not in (0, 1, 2):
            raise ValueError("status must be 0 (pending), 1 (in_progress) or 2 (done)")
        return v

class TaskCreate(TaskBase):
    status: int = 0

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[int] = Field(None, ge=0, le=2)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v not in (0, 1, 2):
            raise ValueError("status must be 0, 1 or 2")
        return v


class TaskOut(TaskBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

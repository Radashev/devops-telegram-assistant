from pydantic import BaseModel
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None


class TaskResponse(TaskBase):
    id: int
    user_id: int
    is_done: bool
    created_at: datetime

    class Config:
        from_attributes = True
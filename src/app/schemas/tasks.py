from pydantic import BaseModel
from typing import List, Optional

class TaskCreate(BaseModel):
    task_name: str
    user_id: int
    prompts: List[str]
    audio_url: Optional[str] = None

class TaskUpdate(BaseModel):
    task_name: Optional[str]
    prompts: Optional[List[str]]

class TaskResponse(BaseModel):
    id: int
    task_name: str
    user_id: int
    prompts: str
    audio_url: Optional[str] = None

    class Config:
        from_attributes = True
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=1000)

class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=1000)
    is_completed: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: str
    updated_at: str

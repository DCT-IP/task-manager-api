from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., example="Learn FastAPI")

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
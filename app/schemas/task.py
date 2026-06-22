from datetime import datetime
from pydantic import BaseModel, Field, field_validator

# 1. Base Shared Fields
class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Title of the task"
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Detailed description"
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError(
                "Title cannot be empty or whitespace"
            )
        return value

# 2. For POST /tasks (Creation)
class TaskCreate(TaskBase):
    pass # Inherits title (required) and description (optional)

# 3. For PATCH /tasks/{id} (Partial Updates)
class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(default=None,max_length=500, description="Detailed description")
    completed: bool | None = Field(default=None)

# 4. For GET /tasks (API Response)
class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    owner_id: int  | None = None

    class Config:
        from_attributes = True
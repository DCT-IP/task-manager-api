from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import re

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(
        from_attributes=True
    )
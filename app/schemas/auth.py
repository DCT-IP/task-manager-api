import re
from pydantic import BaseModel, EmailStr, Field, field_validator

#1. User registeration
class UserRegister(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=30
    )
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if not value.strip():
            raise ValueError(
                "Username cannot be empty or whitespace"
            )
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain an uppercase letter"
            )
        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain a lowercase letter"
            )
        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain a digit"
            )
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError(
                "Password must contain a special character"
            )
        return value

#2. User response 
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


#3. User Login
class UserLogin(BaseModel):
    username: str
    password: str

#4. Login Respone
class LoginResponse(BaseModel):
    message: str

#5. Token Response 
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
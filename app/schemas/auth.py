import re

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    ConfigDict
)


# -------------------------
# USER REGISTRATION
# -------------------------
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
    def validate_username(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Username cannot be empty or whitespace"
            )

        if not re.fullmatch(
            r"[A-Za-z0-9_-]+",
            value
        ):
            raise ValueError(
                "Username contains invalid characters"
            )

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:

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

        if not re.search(
            r"[!@#$%^&*(),.?\":{}|<>]",
            value
        ):
            raise ValueError(
                "Password must contain a special character"
            )

        return value


# -------------------------
# USER RESPONSE
# -------------------------
class UserResponse(BaseModel):

    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )


# -------------------------
# USER LOGIN
# -------------------------
class UserLogin(BaseModel):

    username: str
    password: str


# -------------------------
# TOKEN RESPONSE
# -------------------------
class TokenResponse(BaseModel):

    access_token: str
    token_type: str
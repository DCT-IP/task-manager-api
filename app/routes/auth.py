from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.rate_limiting import limiter
from app.schemas.auth import (
    TokenResponse,
    UserRegister,
    UserResponse,
)

from app.services.auth_service import (
    register_user_service,
    login_user_service
)

from app.core.JWT_handler import create_access_token
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# Register route
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
@limiter.limit("3/minute")
def register_user(
    request: Request,
    user: UserRegister,
    db: Session = Depends(get_db)
):
    created_user = register_user_service(
        db=db,
        username=user.username,
        email=user.email,
        password=user.password
    )

    return created_user


# Login route
@router.post(
    "/login",
    response_model=TokenResponse
)
@limiter.limit("5/minute")
def login_user(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = login_user_service(
        db=db,
        username=form_data.username,
        password=form_data.password
    )

    token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Protected route
@router.get("/me")
@limiter.limit("60/minute")
def get_me(
    request: Request,
    current_user=Depends(get_current_user)
):
    return current_user
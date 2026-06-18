from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.schemas.auth import (
    UserRegister,
    UserResponse,
    UserLogin,
    LoginResponse
)

from app.services.auth_service import (
    register_user_service,
    login_user_service
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register_user(
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

@router.post(
    "/login",
    response_model = LoginResponse
)
def login_user(
    creds: UserLogin,
    db: Session = Depends(get_db)
):
    login_user_service(
        db = db,
        username = creds.username,
        password = creds.password
    )

    return {"message": "Login successful"}
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.schemas.auth import (
    TokenResponse,
    UserRegister,
    UserResponse,
    UserLogin,
    LoginResponse
)

from app.services.auth_service import (
    register_user_service,
    login_user_service
)

from app.core.JWT_handler import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


#register route
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


#Login route
@router.post(
    "/login",
    response_model = TokenResponse
)
def login_user(
    creds: UserLogin,
    db: Session = Depends(get_db)
):
    user = login_user_service(
        db = db,
        username = creds.username,
        password = creds.password
    )
    token = create_access_token(
        data = {"sub": user.username,
                "user_id": user.id
                }
    )

    return {
    "access_token": token,
    "token_type": "bearer"
}


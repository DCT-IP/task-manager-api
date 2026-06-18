from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.schemas.auth import (
    UserRegister,
    UserResponse
)

from app.services.auth_service import (
    register_user_service
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
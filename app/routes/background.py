from fastapi import APIRouter
from fastapi import BackgroundTasks

from app.services.background_service import (
    send_fake_email
)

router = APIRouter(
    prefix="/background",
    tags=["Background Tasks"]
)

@router.post("/email")
def background_email(
    email: str,
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(
        send_fake_email,
        email
    )

    return {
        "message": "Email scheduled"
    }
from fastapi import APIRouter, BackgroundTasks

from app.services.background_service import send_fake_email


router = APIRouter(
    prefix="/background",
    tags=["Background Jobs"]
)


@router.post(
    "/email",
    summary="Send email in background",
    description="Simulates sending an email asynchronously using FastAPI BackgroundTasks."
)
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
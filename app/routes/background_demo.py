from fastapi import APIRouter, BackgroundTasks
from app.logger import logger
import time

router = APIRouter(
    prefix="/background",
    tags=["Background Tasks"]
)


def write_log(message: str):

    time.sleep(5)

    logger.info(
        f"BACKGROUND TASK: {message}"
    )


@router.post("/log")
def background_log(
    message: str,
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(
        write_log,
        message
    )

    return {
        "message": "Background task scheduled"
    }
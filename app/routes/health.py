from fastapi import APIRouter
from sqlalchemy import text

from app.database import engine
from app.core.redis_client import redis_client

router = APIRouter(
    prefix="/health",
    tags=["System Health"]
)


@router.get(
    "",
    summary="Check ssystem health",
    description="Checks database and Redis connectivity and returns overall system status."
)
def health_check():
    db_status = "down"
    redis_status = "down"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "up"
    except Exception:
        pass
    try:
        redis_client.ping()
        redis_status = "up"
    except Exception:
        pass
    overall = (
        "healthy"
        if db_status == "up" and redis_status == "up"
        else "degraded"
    )
    return {
        "status": overall,
        "database": db_status,
        "redis": redis_status
    }
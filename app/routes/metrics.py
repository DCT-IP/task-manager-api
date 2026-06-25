import time
from fastapi import APIRouter

router = APIRouter(
    prefix="/metrics",
    tags=["Observability"]
)

start_time = time.time()
request_count = 0


def increment_request():
    global request_count
    request_count += 1


def get_request_count():
    return request_count


@router.get(
    "/",
    summary="Get system metrics",
    description="Returns basic runtime metrics like uptime and total request count for observability."
)
def get_metrics():
    uptime = time.time() - start_time

    return {
        "uptime_seconds": uptime,
        "requests_total": get_request_count(),
        "status": "active"
    }
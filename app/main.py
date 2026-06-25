import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import Request
from fastapi.staticfiles import StaticFiles

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.core.config import settings
from app.core.rate_limiting import limiter

from app.logger import logger
from app.database import engine, Base
from app.models import user, task

from app.middleware.security_headers import SecurityHeadersMiddleware

from app.routes.health import router as health_router
from app.routes.tasks import router as tasks_router
from app.routes.auth import router as auth_router
from app.routes.background import router as background_router
from app.routes.metrics import router as metrics_router


app = FastAPI(
    title=settings.APP_NAME,
    description="Simple API for managing tasks",
    version="1.0.0"
)

API_PREFIX = "/api/v1"


request_count = 0
start_time = time.time()
total_latency = 0.0


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(SecurityHeadersMiddleware)


@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    logger.info(
        f"{request.method} {request.url.path} {response.status_code} {duration:.4f}s"
    )

    return response


@app.middleware("http")
async def metrics_middleware(request, call_next):
    global request_count, total_latency

    request_count += 1

    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    total_latency += duration

    response.headers["X-Response-Time"] = str(duration)

    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/frontend"), name="static")

app.include_router(tasks_router, prefix=API_PREFIX)
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(health_router, prefix=API_PREFIX)
app.include_router(background_router, prefix=API_PREFIX)
app.include_router(metrics_router, prefix=API_PREFIX)


@app.get("/", tags=["System"])
def root():
    return FileResponse("app/frontend/index.html")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.routes.tasks import router as tasks_router
from app.routes.auth import router as auth_router

from app.database import engine, Base
from app.models import user, task   # IMPORTANT: registers models
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Simple API for managing tasks",
    version="1.0.0"
)

# -------------------------
# DATABASE INITIALIZATION
# -------------------------
Base.metadata.create_all(bind=engine)

# -------------------------
# CORS MIDDLEWARE
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ROUTES
# -------------------------
app.include_router(tasks_router)
app.include_router(auth_router)

# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/")
def root():
    return {"message": "API is running"}

# -------------------------
# SIMPLE FRONTEND (optional)
# -------------------------
@app.get("/ui")
def serve_ui():
    return FileResponse("app/frontend/index.html")

@app.get("/debug/tasks")
def debug_tasks():
    from app.database import SessionLocal
    db = SessionLocal()
    return db.query(task.Task).all()
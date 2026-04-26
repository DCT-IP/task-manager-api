from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from fastapi.responses import FileResponse
from app.routes.tasks import router as tasks_router
from app.routes.auth import router as auth_router

app = FastAPI(
    title="Task Manager API",
    description="Simple API for managing tasks",
    version="1.0.0"
)

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/ui")
def serve_ui():
    return FileResponse("app/frontend/index.html")
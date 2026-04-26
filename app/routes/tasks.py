from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Fake DB
tasks_db = []


# CREATE
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    task_data = {
        "id": len(tasks_db),
        "title": task.title,
        "completed": False
    }
    tasks_db.append(task_data)
    return task_data


# READ ALL
@router.get("/", response_model=List[TaskResponse])
def get_tasks():
    return tasks_db


# READ ONE
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    if task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]


# DELETE
@router.delete("/{task_id}")
def delete_task(task_id: int):
    if task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db.pop(task_id)
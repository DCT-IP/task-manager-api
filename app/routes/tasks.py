from fastapi import APIRouter, HTTPException, Depends
from typing import List
import asyncio
import time
import httpx
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# -------------------------
# CREATE TASK
# -------------------------
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = Task(
        title=task.title,
        completed=False
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# -------------------------
# GET ALL TASKS
# -------------------------
@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# -------------------------
# ASYNC NON-BLOCKING ENDPOINT
# -------------------------
@router.get("/slow")
async def slow_endpoint():
    print("START")
    for i in range(5):
        print(f"working {i}")
        await asyncio.sleep(1)
    print("END")
    return {"message": "Async endpoint completed"}


# -------------------------
# BLOCKING ENDPOINT
# -------------------------
@router.get("/blocking")
def blocking_endpoint():
    print("Blocking request started")
    time.sleep(5)
    print("Blocking request finished")
    return {"message": "Blocking endpoint completed"}

# -------------------------
# EXTERNAL API CALL
# -------------------------
@router.get("/external")
async def external_api_test():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://jsonplaceholder.typicode.com/todos/1"
        )
    data = response.json()
    return {
        "external_data": data
    }

@router.get("/multi-external")
async def multi_external():
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(1, 6):
            tasks.append(
                client.get(
                    f"https://jsonplaceholder.typicode.com/todos/{i}"
                )
            )
        responses = await asyncio.gather(*tasks)
    results = []
    for response in responses:
        results.append(response.json())
    return {"results": results}

# -------------------------
# GET SINGLE TASK
# -------------------------
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task

# -------------------------
# DELETE TASK
# -------------------------
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

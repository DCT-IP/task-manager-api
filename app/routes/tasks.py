import asyncio
import time
from typing import List
import httpx
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import (
    create_task_service,
    get_tasks_service,
    get_task_service,
    delete_task_service,
    update_task_service
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# -------------------------
# CREATE TASK
# -------------------------
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task_service(db, task)


# -------------------------
# GET ALL TASKS
# -------------------------
@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return get_tasks_service(db)


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
    time.sleep(5)  # Runs safely in a thread pool because this is a standard 'def'
    print("Blocking request finished")
    return {"message": "Blocking endpoint completed"}


# -------------------------
# EXTERNAL API CALL
# -------------------------
@router.get("/external")
async def external_api_test():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos/1")
    return {"external_data": response.json()}


@router.get("/multi-external")
async def multi_external():
    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(f"https://jsonplaceholder.typicode.com/todos/{i}") 
            for i in range(1, 6)
        ]
        responses = await asyncio.gather(*tasks)
    
    results = [response.json() for response in responses]
    return {"results": results}


# -------------------------
# GET SINGLE TASK
# -------------------------
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_service(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# -------------------------
# DELETE TASK
# -------------------------
# FIXED: Removed the unnecessary task_data payload requirement
@router.delete("/{task_id}", status_code=200)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_service(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    delete_task_service(db, task)
    return {"message": "Task deleted"}


# -------------------------
# UPDATE TASK
# -------------------------
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    task = get_task_service(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return update_task_service(db, task, task_data)
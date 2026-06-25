import asyncio
import time
from typing import List
from app.core.metrics import increment_counter
import httpx
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from app.core.rate_limiting import limiter
from app.dependencies.auth import get_current_user
from app.database import get_db
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
@router.post(
    "/",
    response_model=TaskResponse,
    status_code=201
)
@limiter.limit("20/minute")
def create_task(
    request: Request,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return create_task_service(
        db,
        task,
        owner_id=current_user["user_id"]
    )


# -------------------------
# GET ALL TASKS
# -------------------------
@router.get("/", response_model=List[TaskResponse])
@limiter.limit("60/minute")
def get_tasks(
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_tasks_service(
        db,
        user_id=current_user["user_id"]
    )


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
    return {
        "message": "Async endpoint completed"
    }


# -------------------------
# BLOCKING ENDPOINT
# -------------------------
@router.get("/blocking")
def blocking_endpoint():
    print("Blocking request started")

    time.sleep(5)

    print("Blocking request finished")

    return {
        "message": "Blocking endpoint completed"
    }


# -------------------------
# EXTERNAL API CALL
# -------------------------
@router.get("/external")
@limiter.limit("30/minute")
async def external_api_test(
    request: Request
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://jsonplaceholder.typicode.com/todos/1"
        )

    return {
        "external_data": response.json()
    }


# -------------------------
# MULTIPLE EXTERNAL API CALLS
# -------------------------
@router.get("/multi-external")
@limiter.limit("20/minute")
async def multi_external(
    request: Request
):
    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(
                f"https://jsonplaceholder.typicode.com/todos/{i}"
            )
            for i in range(1, 6)
        ]

        responses = await asyncio.gather(*tasks)

    results = [
        response.json()
        for response in responses
    ]

    return {
        "results": results
    }

#demo
@router.get("/redis-limit-demo")
def redis_limit_demo(
    current_user: dict = Depends(get_current_user)
):
    count = increment_counter(
        current_user["user_id"]
    )

    return {
        "requests_this_minute": count
    }
# -------------------------
# GET SINGLE TASK
# -------------------------
@router.get("/{task_id}", response_model=TaskResponse)
@limiter.limit("60/minute")
def get_task(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    task = get_task_service(
        db,
        task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.owner_id != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return task


# -------------------------
# UPDATE TASK
# -------------------------
@router.put("/{task_id}", response_model=TaskResponse)
@limiter.limit("20/minute")
def update_task(
    request: Request,
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    task = get_task_service(
        db,
        task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.owner_id != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return update_task_service(
        db,
        task_id,
        task_update
    )


# -------------------------
# DELETE TASK
# -------------------------
@router.delete("/{task_id}", status_code=200)
@limiter.limit("20/minute")
def delete_task(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    task = get_task_service(
        db,
        task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.owner_id != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    delete_task_service(
        db,
        task
    )

    return {
        "message": "Task deleted"
    }


from fastapi import APIRouter, HTTPException, Depends
from typing import List

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
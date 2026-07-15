from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.logger import logger
import json
from app.core.redis_client import redis_client
from app.core.metrics import increment_counter
# -------------------------
# CREATE TASK AND LOG
# -------------------------

def create_task_service(db: Session, task_data: TaskCreate, owner_id: int) -> Task:
    logger.info("Creating a new task")
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        owner_id=owner_id,
        completed=False
    )
    db.add(new_task)
    try:
      db.commit()
    except Exception as e:
        db.rollback()
        logger.exception(f"Failed to create task: {e}")
        raise 
    db.refresh(new_task)
    #redis_client.delete(f"tasks:{owner_id}")
    logger.info(f"Task created with ID: {new_task.id}")
    return new_task


# -------------------------
# GET ALL TASKS AND LOG
# -------------------------
def get_tasks_service(db: Session, user_id: int):
    tasks = (
        db.query(Task)
        .filter(Task.owner_id == user_id)
        .all()
    )

    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "owner_id": task.owner_id,
            "created_at": task.created_at.isoformat() if task.created_at else None
        }
        for task in tasks
    ]


# -------------------------
# GET SINGLE TASK AND LOG
# -------------------------
def get_task_service(db: Session, task_id: int) -> Task | None:
    logger.info(f"Fetching task with ID: {task_id}")
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        logger.info(f"Task found with ID: {task.id}")
    else:
        logger.warning(f"Task not found with ID: {task_id}")
    return task


# -------------------------
# DELETE TASK AND LOG
# -------------------------
def delete_task_service(db: Session, task: Task) -> None:
    logger.info(f"Deleting task with ID: {task.id}")
    db.delete(task)
    db.commit()
    redis_client.delete(
    f"tasks:{task.owner_id}")
    logger.info(f"Task deleted with ID: {task.id}")


# -------------------------
# UPDATE TASK AND LOG
# -------------------------
def update_task_service(
    db: Session,
    task_id: int,
    task_data: TaskUpdate
):
    logger.info(f"Updating task with ID: {task_id}")
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()
    if not task:
        return None
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed
    db.commit()
    redis_client.delete(
    f"tasks:{task.owner_id}"
    )
    db.refresh(task)
    logger.info(f"Task updated with ID: {task.id}")
    return task

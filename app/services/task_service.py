from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.logger import logger

# -------------------------
# CREATE TASK AND LOG
# -------------------------
logger.info("Creating a new task")
def create_task_service(db: Session, task_data: TaskCreate, owner_id: int) -> Task:
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
        logger.exception(f"Failed to create task: {e}")
    db.refresh(new_task)
    logger.info(f"Task created with ID: {new_task.id}")
    return new_task


# -------------------------
# GET ALL TASKS AND LOG
# -------------------------
def get_tasks_service(db: Session) -> list[Task]:
    logger.info("Fetching all tasks")
    tasks = db.query(Task).all()
    logger.info(f"Retrieved {len(tasks)} tasks")
    return tasks


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
    db.refresh(task)
    logger.info(f"Task updated with ID: {task.id}")
    return task
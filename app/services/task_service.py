from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate


# -------------------------
# CREATE TASK
# -------------------------
def create_task_service(
    db: Session,
    task_data: TaskCreate
):
    new_task = Task(
        title=task_data.title,
        completed=False
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# -------------------------
# GET ALL TASKS
# -------------------------
def get_tasks_service(db: Session):
    return db.query(Task).all()


# -------------------------
# GET SINGLE TASK
# -------------------------
def get_task_service(
    db: Session,
    task_id: int
):
    return db.query(Task).filter(
        Task.id == task_id
    ).first()


# -------------------------
# DELETE TASK
# -------------------------
def delete_task_service(
    db: Session,
    task: Task
):
    db.delete(task)
    db.commit()

# -------------------------
# UPDATE TASK
# -------------------------
def update_task_service(
        db: Session,
        task: Task,
        task_data
):
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.completed is not None:
        task.completed = task_data.completed
    db.commit()
    db.refresh(task)
    return task

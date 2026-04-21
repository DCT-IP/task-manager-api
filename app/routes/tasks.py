from fastapi import APIRouter
from pydantic import BaseModel

task_db=[] #for now tasks stored here 

class Task(BaseModel):
    title: str
router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", status_code=201)
def create_task(task: Task):
    task_db.append(task)
    return {"message": "Task created", "task": task}

@router.get("/")
def get_tasks():
    return task_db
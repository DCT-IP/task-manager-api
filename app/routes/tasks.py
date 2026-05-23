from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])     #prepends /task to all routes to save time and avoid repetition
#the tags argument is to document all the routes in the file as tasks in docs

tasks_db = []
current_id = 0


# CREATE
@router.post("/", response_model=TaskResponse, status_code=201) #status code 201 means created 
def create_task(task: TaskCreate):
    global current_id
    task_data = {
        "id": current_id,
        "title": task.title,
        "completed": False
    }
    tasks_db.append(task_data)
    current_id += 1
    return task_data
# frontend sends POST request to /tasks with JSON with a title, body and status


# GET ALL
@router.get("/", response_model=List[TaskResponse])
def get_tasks():
    return tasks_db
#A get request to tasks simply hands entire tasks_db list

# GET ONE
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")
#A get request to /tasks/{task_id} loops through tasks_db to find a task with the matching id and returns it, otherwise raises 404 error

# DELETE
@router.delete("/{task_id}")
def delete_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            tasks_db.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
#A delete request to /tasks/{task_id} loops through tasks_db to find a task with the matching id and removes it, otherwise raises 404 error
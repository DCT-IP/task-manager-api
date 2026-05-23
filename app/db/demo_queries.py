from app.database import SessionLocal
from app.models.user import User
from app.models.task import Task

db = SessionLocal()

# --------------------
# CREATE USER
# --------------------
user = User(
    username="testuser",
    email="test@mail.com",
    password_hash="hashed_password"
)

db.add(user)
db.commit()
db.refresh(user)

print("User created:", user.id)

# --------------------
# CREATE TASK
# --------------------
task = Task(
    title="Learn FastAPI",
    user_id=user.id
)

db.add(task)
db.commit()

print("Task created")

# --------------------
# READ TASKS
# --------------------
tasks = db.query(Task).all()
print(tasks)

# --------------------
# FILTER TASKS
# --------------------
user_tasks = db.query(Task).filter(Task.user_id == user.id).all()
print(user_tasks)
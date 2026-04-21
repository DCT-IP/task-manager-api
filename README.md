# Task Manager API

A simple REST API built using FastAPI to manage tasks.  
This project is part of a backend learning roadmap focusing on API design, async programming, and database integration.

---

## Features

- Create tasks
- Get all tasks
- Get a task by ID
- Delete tasks
- Auto-generated API documentation (Swagger)

---

## Tech Stack

- FastAPI
- Uvicorn
- Pydantic


---


##  Running the Project

1. Clone the repo:
```bash
git clone <your-repo-link>
cd task-manager-api
```

2.Create venv
```python
python -m venv venv
```
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3.Install required dependencies
 pip install

4.Run server
 uvicorn app.main:app --reload

---


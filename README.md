# Task Manager API

A production-oriented REST API built with FastAPI for task management.

This project is part of a backend engineering roadmap focused on API development, security, testing, database management, and DevOps practices.

---

## Features

### Task Management

* Create tasks
* Retrieve all tasks
* Retrieve a task by ID
* Update tasks
* Delete tasks

### Authentication & Authorization

* JWT Authentication
* User Registration & Login
* Protected Endpoints
* Task Ownership Enforcement

### Security

* Password Hashing
* Rate Limiting
* Security Headers
* Input Validation
* Validation Hardening

### Database

* MySQL Integration
* SQLAlchemy ORM
* Alembic Database Migrations

### DevOps

* Dockerized Application
* Docker Compose Orchestration
* GitHub Actions CI
* Environment Variable Configuration
* Automated Test Suite

### CI/CD

* This project uses GitHub Actions for Continuous Integration.

* On every push and pull request to `main`:

  - A MySQL service container is started
  - Environment variables are injected
  - Alembic migrations are applied
  - Automated tests are executed using Pytest

* This ensures changes are validated automatically before being merged.

* Workflow location:

.github/workflows/ci.yml

---

## Tech Stack

### Backend

* FastAPI
* Uvicorn
* SQLAlchemy
* PyMySQL
* Pydantic

### Security

* Passlib
* bcrypt
* python-jose

### Database

* MySQL
* Alembic

### Testing

* Pytest
* HTTPX

### DevOps

* Docker
* GitHub Actions CI
* Render Deployment
* Railway MySQL

---

## Project Structure

```text
task-manager-api/
│
├── app/
│   ├── core/
│   ├── dependencies/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── tests/
├── alembic/
├── docs/
│
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
├── .env.example
└── README.md
```

---

## Local Setup

### Clone Repository

```bash
git clone <repository-url>
cd task-manager-api
```

### Create Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / Mac:

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file using `.env.example`.

Example:

```env
APP_NAME=Task Manager API

DATABASE_URL=mysql+pymysql://api_user:password@localhost:3306/taskdb

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run Application

```bash
uvicorn app.main:app --reload
```

Application:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

ReDoc Documentation:

```text
http://localhost:8000/redoc
```

---

## Docker Setup

Build and run:

```bash
docker compose up --build
```

Stop containers:

```bash
docker compose down
```

---

## Database Migrations

Create migration:

```bash
alembic revision --autogenerate -m "migration_name"
```

Apply migration:

```bash
alembic upgrade head
```

Check migration status:

```bash
alembic current
```

---

## Testing

Run all tests:

```bash
pytest -v
```

Current test coverage includes:

* Authentication
* Authorization
* Task Ownership
* CRUD Operations
* Rate Limiting
* Security Headers
* Input Validation
* Validation Hardening

---

## Deployment

Production API:
https://task-manager-api-cvf6.onrender.com

Interactive API Documentation:
https://task-manager-api-cvf6.onrender.com/docs

---

## Learning Goals

This project is being used to learn:

* FastAPI
* REST API Design
* Authentication & Authorization
* Secure Backend Development
* SQLAlchemy ORM
* Database Migrations
* Docker
* Testing
* CI/CD
* Redis Caching
* Async Programming
* Background Tasks

---
## Completed:

* FastAPI
* REST API Design
* Authentication & Authorization
* SQLAlchemy ORM
* Database Migrations
* Docker
* Testing
* CI
* Deployment/CD

---
## Currently Exploring:

* Redis Caching
* Async Programming
* Background Tasks

---
## License

This project is licensed under the MIT License.

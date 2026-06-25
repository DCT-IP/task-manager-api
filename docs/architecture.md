# Task Manager API — Architecture Overview

## Live Links

API:
https://task-manager-api-cvf6.onrender.com/

Documentation:
https://task-manager-api-cvf6.onrender.com/docs

---

# System Architecture

```text
                         Client
                            │
                            ▼
                  ┌─────────────────┐
                  │ FastAPI App     │
                  │ (Uvicorn ASGI)  │
                  └────────┬────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼

 ┌────────────────┐ ┌───────────────┐ ┌────────────────┐
 │ Middleware     │ │ API Routers   │ │ OpenAPI Docs   │
 │                │ │               │ │ (/docs)        │
 │ • CORS         │ │ • Auth        │ └────────────────┘
 │ • Rate Limit   │ │ • Tasks       |
 │ • Security     │ │ • Health      |
 │ • Logging      │ │ • Metrics     |
 │ • Metrics      │ │ • Background  |
 └───────┬────────┘ └───────┬───────┘
         │                  │
         ▼                  ▼

 ┌────────────────────────────────────┐
 │         Service Layer              │
 │                                    │
 │ • Authentication Logic             │
 │ • Task Business Logic              │
 │ • Background Job Logic             │
 └───────────────┬────────────────────┘
                 │
      ┌──────────┴──────────┐
      │                     │
      ▼                     ▼

┌──────────────┐    ┌────────────────┐
│ Redis        │    │ SQLAlchemy ORM │
│              │    │                │
│ • Rate Data  │    │ Database Access│
│ • Health     │    └───────┬────────┘
└──────────────┘            │
                            ▼

                    ┌─────────────┐
                    │ MySQL       │
                    │ Database    │
                    └─────────────┘
```

---

# Request Flow

```text
Client Request
      │
      ▼
Middleware Layer
      │
      ├── Security Headers
      ├── Rate Limiting
      ├── Request Logging
      └── Metrics Collection
      │
      ▼
API Route
      │
      ▼
Authentication Check
      │
      ▼
Service Layer
      │
      ├── Redis Operations
      └── Database Operations
      │
      ▼
Response
```

---

# Core Components

## Authentication

Implemented using JWT tokens.

Flow:

```text
Register User
      │
      ▼
Password Hashing (bcrypt)
      │
      ▼
Store User in MySQL

Login
      │
      ▼
Credential Validation
      │
      ▼
JWT Generation
      │
      ▼
Protected Endpoints
```

### Features

- User registration
- User login
- JWT authentication
- Protected routes
- Ownership-based authorization

---

## Task Management

Supported operations:

- Create task
- View tasks
- View single task
- Update task
- Delete task

Ownership checks ensure users can only access their own tasks.

---

## Rate Limiting

Implemented using:

- SlowAPI
- Redis backend

Examples:

```text
Register → 3/min
Login    → 5/min
Tasks    → endpoint-specific limits
```

Purpose:

- Prevent abuse
- Protect authentication endpoints
- Demonstrate distributed rate limiting

---

## Observability

### Health Endpoint

```text
/api/v1/health
```

Checks:

- MySQL connectivity
- Redis connectivity

Example response:

```json
{
  "status": "healthy",
  "database": "up",
  "redis": "up"
}
```

---

### Metrics Endpoint

```text
/api/v1/metrics
```

Provides:

- Application uptime
- Request count
- Service status

Example response:

```json
{
  "uptime_seconds": 12345,
  "requests_total": 500,
  "status": "active"
}
```

---

## Background Tasks

Endpoint:

```text
/api/v1/background/email
```

Uses FastAPI BackgroundTasks to execute work after the response has been returned.

Demonstrates:

- Non-blocking task execution
- Separation of user response from secondary work

---

## Async Demonstrations

Learning endpoints:

```text
/api/v1/tasks/slow
/api/v1/tasks/blocking
/api/v1/tasks/external
/api/v1/tasks/multi-external
```

These demonstrate:

- asyncio
- async HTTP requests
- concurrent execution
- blocking vs non-blocking behavior

---

# Infrastructure

## Database

- MySQL
- SQLAlchemy ORM
- Alembic migrations

## Cache / Supporting Services

- Redis
- Rate-limiting storage
- Health monitoring

## Deployment

Application:
https://task-manager-api-cvf6.onrender.com/

Documentation:
https://task-manager-api-cvf6.onrender.com/docs

---

# CI Pipeline

GitHub Actions executes:

```text
Push / Pull Request
          │
          ▼
Install Dependencies
          │
          ▼
Run Alembic Migrations
          │
          ▼
Run Pytest Suite
          │
          ▼
Report Status
```

Current automated coverage includes:

- Authentication
- Authorization
- Task CRUD
- Ownership checks
- Validation
- Rate limiting
- Background routes
- Health endpoints

---

# Learning Outcomes

This project was used to gain hands-on experience with:

- FastAPI
- REST API Design
- JWT Authentication
- Authorization
- SQLAlchemy
- Alembic
- MySQL
- Redis
- AsyncIO
- Background Tasks
- Docker
- CI/CD
- Automated Testing
- API Documentation
- Production Deployment

---

# Project Status

Version: v1.0.0

The project is considered feature-complete for its learning objectives and serves as a production-oriented backend engineering portfolio project.
# API Overview

## Introduction
The Task Manager API provides authenticated users with the ability to manage personal tasks through a RESTful interface.

The API supports:

* User Registration
* User Authentication
* Task Creation
* Task Retrieval
* Task Updates
* Task Deletion

Base URL:
```text
http://localhost:8000
```

Authentication:
```text
Bearer JWT Token
```

---

## Authentication Endpoints

### Register User
```http
POST /auth/register
```
Creates a new user account.
Request Body:
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "Password123!"
}
```

Response:
```json
{
  "message": "User registered successfully"
}
```
---

### Login
```http
POST /auth/login
```
Authenticates a user and returns an access token.

Request:
```text
username=john
password=Password123!
```

Response:
```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

---

## Task Endpoints

All task endpoints require authentication.

---

### Create Task

```http
POST /tasks
```

Request:

```json
{
  "title": "Complete FastAPI project",
  "description": "Finish documentation"
}
```

---

### Get All Tasks

```http
GET /tasks
```

Returns all tasks belonging to the authenticated user.

---

### Get Task By ID

```http
GET /tasks/{id}
```

Returns a specific task if owned by the authenticated user.

---

### Update Task

```http
PUT /tasks/{id}
```

Example:

```json
{
  "title": "Updated Task",
  "completed": true
}
```

---

### Delete Task

```http
DELETE /tasks/{id}
```

Deletes the specified task.

---

## Security Features

The API includes:

* JWT Authentication
* Ownership-Based Authorization
* Password Hashing
* Rate Limiting
* Security Headers
* Input Validation

---

## Interactive Documentation

FastAPI automatically generates API documentation.

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

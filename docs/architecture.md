# Architecture Overview
## Project Summary

Task Manager API is a production-oriented REST API built using FastAPI and MySQL.
The project was developed as part of a backend engineering roadmap focused on API development, authentication, authorization, database management, testing, containerization, and DevOps practices.
The application allows authenticated users to create, manage, update, and delete their own tasks while enforcing ownership-based access control.

---

## Core Features

### Task Management
* Create Tasks
* View Tasks
* Update Tasks
* Delete Tasks
* Track Completion Status

### Authentication & Authorization
* User Registration
* User Login
* JWT Authentication
* Protected Endpoints
* Ownership-Based Access Control

### Security
* Password Hashing
* Security Headers Middleware
* Input Validation
* Rate Limiting

### DevOps
* Dockerized Application
* Docker Compose
* Alembic Migrations
* GitHub Actions CI

---

## High-Level Architecture
```text
Client
  │
  ▼
FastAPI Routes
  │
  ▼
Dependencies
(Authentication / Authorization)
  │
  ▼
Service Layer
  │
  ▼
SQLAlchemy ORM
  │
  ▼
MySQL Database
```

Supporting Components:
``` text
JWT Authentication
Security Headers Middleware
Rate Limiting
Alembic Migrations
Docker
GitHub Actions CI
```

---

## Application Structure
```text
app/
├── core/           # Configuration, authentication, rate limiting
├── db/             # Database session management
├── dependencies/   # Dependency injection utilities
├── frontend/       # Minimal frontend client
├── middleware/     # Security middleware
├── models/         # Database models
├── routes/         # API endpoints
├── schemas/        # Request/response validation
├── services/       # Business logic
└── main.py
```
The project follows a layered architecture that separates routing, business logic, and persistence logic.

---

## Request Flow
A typical API request follows the path below:

```text
Client Request
      │
      ▼
FastAPI Route
      │
      ▼
Authentication Check
      │
      ▼
Authorization Check
      │
      ▼
Service Layer
      │
      ▼
Database Operations
      │
      ▼
JSON Response
```

---
## Authentication Flow

The application uses JWT-based authentication.
### User Registration

```text
Client
  │
  ▼
POST /auth/register
  │
  ▼
Password Hashing
  │
  ▼
Store User
```
Passwords are never stored in plaintext.

---

### User Login
```text
Client Credentials
        │
        ▼
POST /auth/login
        │
        ▼
Credential Validation
        │
        ▼
JWT Token Generated
```
Successful authentication returns a JWT access token.

---

### Protected Requests
```text
JWT Token
     │
     ▼
Authorization Header
     │
     ▼
Token Validation
     │
     ▼
Current User Retrieved
```
Authenticated endpoints require a valid JWT token before any business logic is executed.

---

## Authorization Model
Authentication identifies the user.
Authorization determines which resources a user can access.
The API enforces task ownership.
Example:
```text
User A creates Task #1

User B attempts:

GET /tasks/1
PUT /tasks/1
DELETE /tasks/1

Result:
Access Denied
```
Users can only interact with tasks they own.

---

## Database Design

### User Model
```text
User
├── id
├── username
├── email
└── password_hash
```

### Task Model
```text
Task
├── id
├── title
├── description
├── completed
├── created_at
└── owner_id
```

### Relationship
```text
One User
     │
     ▼
Many Tasks
```
The relationship is implemented using SQLAlchemy ORM relationships and foreign keys.

---

## Security Architecture

### Password Storage
User passwords are hashed before being stored in the database.

### Security Headers
Every response includes security-focused HTTP headers:

* X-Content-Type-Options
* X-Frame-Options
* Referrer-Policy
* Permissions-Policy

These headers help reduce common browser-based attack vectors.

### Rate Limiting
Rate limiting is applied to protect endpoints from excessive request volume and abuse.

---

## Database Migration Strategy
Database schema changes are managed through Alembic.

Migration workflow:
```text
Model Changes
      │
      ▼
Alembic Revision
      │
      ▼
Migration Script
      │
      ▼
Database Upgrade
```
This enables reproducible schema evolution across environments.

---

## Testing Strategy
Automated testing is implemented using Pytest.

Coverage includes:

* Authentication
* Authorization
* Task Ownership
* CRUD Operations
* Input Validation
* Security Headers
* Rate Limiting

Tests run automatically through GitHub Actions on every push and pull request.

---

## CI Pipeline
The project uses GitHub Actions for Continuous Integration.

Pipeline Flow:

```text
Developer Push
       │
       ▼
GitHub Actions
       │
       ▼
MySQL Service Container
       │
       ▼
Alembic Migrations
       │
       ▼
Pytest
       │
       ▼
Pass / Fail
```

This prevents unverified code from being merged into the main branch.

---

## Containerization
The application is fully containerized using Docker and Docker Compose.
Services:
```text
api
└── FastAPI Application
db
└── MySQL Database
```
Docker Compose orchestrates communication between the application and database containers.

---
## Future Enhancements
Planned improvements include:

* Continuous Deployment (CD)
* Production Deployment
* Redis Caching
* Background Tasks
* Async Database Operations
* Monitoring and Observability

```
```

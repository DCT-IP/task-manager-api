# CI/CD Pipeline

## Overview

The Task Manager API uses GitHub Actions to automate verification of code changes.

The current implementation includes Continuous Integration (CI).

Continuous Deployment (CD) is planned as a future enhancement.

---

## Continuous Integration (CI)

The CI pipeline automatically runs whenever code is pushed to the repository or when a pull request is opened against the main branch.

### Workflow Triggers

```text
Push to Main Branch
Pull Request to Main Branch
```

### CI Pipeline Flow

```text
Developer Push
       │
       ▼
GitHub Actions
       │
       ▼
Provision MySQL Service
       │
       ▼
Install Dependencies
       │
       ▼
Run Alembic Migrations
       │
       ▼
Execute Pytest Suite
       │
       ▼
Pass / Fail Result
```

---

## Pipeline Components

### Source Control

GitHub is used for version control and collaboration.

All changes are tracked through commits, branches, and pull requests.

---

### GitHub Actions

GitHub Actions serves as the automation platform responsible for executing the CI workflow.

Responsibilities:

* Environment Setup
* Dependency Installation
* Database Provisioning
* Migration Execution
* Automated Testing

---

### Database Service

A temporary MySQL service container is provisioned during workflow execution.

Configuration includes:

```text
Database: taskdb
User: api_user
Engine: MySQL 8
```

This provides a clean and reproducible test environment.

---

### Alembic Migrations

Before tests are executed, database migrations are applied automatically.

```bash
alembic upgrade head
```

This ensures the database schema matches the current application version.

---

### Automated Testing

The test suite is executed using Pytest.

Command:

```bash
pytest -v
```

Coverage includes:

* Authentication
* Authorization
* Ownership Validation
* CRUD Operations
* Rate Limiting
* Security Headers
* Input Validation

Only changes that pass all automated checks are considered verified.

---

## Benefits

The CI pipeline provides:

* Early Bug Detection
* Automated Regression Prevention
* Consistent Test Execution
* Reproducible Environments
* Improved Code Quality

---

## Current State

Implemented:

```text
✓ GitHub Actions
✓ MySQL Service Container
✓ Alembic Migration Execution
✓ Automated Testing
✓ Pull Request Validation
```

Planned:

```text
□ Continuous Deployment
□ Automated Production Releases
□ Deployment Health Checks
□ Rollback Strategy
```

---

## Future Continuous Deployment (CD)

The next phase of the project is Continuous Deployment.

Target workflow:

```text
Developer Push
       │
       ▼
GitHub Actions
       │
       ▼
Automated Tests
       │
       ▼
Build Docker Image
       │
       ▼
Deploy Application
       │
       ▼
Health Check
       │
       ▼
Production Environment
```

This will allow validated changes to be deployed automatically after successful CI execution.

---

## Future Infrastructure Goals

Planned improvements include:

* Continuous Deployment
* Cloud Hosting
* Redis Integration
* Monitoring and Logging
* Background Task Processing
* Production Observability

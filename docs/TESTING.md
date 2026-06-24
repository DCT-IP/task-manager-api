# Testing Strategy

## Overview

The Task Manager API includes an automated test suite built using Pytest.

The goal of the test suite is to verify application correctness, security controls, authorization rules, and API behavior before changes are merged.

Tests execute automatically through GitHub Actions on every push and pull request.

---

## Testing Stack

### Frameworks

* Pytest
* FastAPI TestClient
* HTTPX

### Execution

```bash
pytest -v
```

---

## Test Categories

### Authentication Tests

Authentication tests verify that users can register, log in, and receive valid JWT access tokens.

Coverage includes:

* User Registration
* User Login
* Invalid Credentials
* JWT Token Generation
* Protected Endpoint Access

---

### Authorization Tests

Authorization tests verify that authenticated users can only access resources they own.

Coverage includes:

* Access Control Enforcement
* Unauthorized Resource Access
* Ownership Validation

Example:

```text
User A creates a task.

User B attempts:
GET /tasks/{id}
PUT /tasks/{id}
DELETE /tasks/{id}

Expected Result:
Access Denied
```

---

### CRUD Tests

Task management functionality is tested end-to-end.

Coverage includes:

* Create Task
* Retrieve Task
* Retrieve Task List
* Update Task
* Delete Task

These tests ensure database operations behave as expected.

---

### Validation Tests

Input validation is verified using invalid request payloads.

Coverage includes:

* Missing Fields
* Invalid Data Types
* Empty Inputs
* Schema Validation

---

### Security Header Tests

The application includes custom security middleware.

Tests verify the presence of:

* X-Content-Type-Options
* X-Frame-Options
* Referrer-Policy
* Permissions-Policy

These headers help reduce common browser-based attack vectors.

---

### Rate Limiting Tests

Rate limiting controls are tested to ensure excessive requests are restricted.

Coverage includes:

* Allowed Requests
* Rate Limit Exceeded Responses

This helps protect the API from abuse and accidental overload.

---

## Test Environment

Tests run against an isolated database environment.

A new user is generated dynamically during testing to avoid conflicts between test executions.

Example:

```text
user_a1b2c3
user_d4e5f6
user_x7y8z9
```

This allows tests to remain independent and repeatable.

---

## Continuous Integration

Automated tests are executed through GitHub Actions.

Pipeline:

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

Code changes are automatically validated before integration into the main branch.

---

## Future Improvements

Planned testing enhancements include:

* Coverage Reporting
* Integration Testing
* Docker-Based Test Execution
* Performance Testing
* Load Testing



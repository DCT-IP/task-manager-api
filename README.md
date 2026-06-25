# Task Manager API

A high-performance, asynchronous REST API built with FastAPI, engineered for secure task operations, enterprise-grade observability, and automated infrastructure deployment. 

This system serves as a showcase of advanced backend engineering practices, focusing on system architecture design, distributed caching, containerized orchestration, and rigorous continuous integration (CI) pipelines.

---

## System Architecture

The application is structured as a decoupled, multi-layered architecture designed to maximize horizontal scaling, optimize database traffic via distributed caching, and handle long-running operations asynchronously.

       ┌────────────────────────────────────────────────────────┐
       │                   Client Request                       │
       └──────────────────────────┬─────────────────────────────┘
                                  │
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │             Uvicorn ASGI Web Server                    │
       └──────────────────────────┬─────────────────────────────┘
                                  │
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │           FastAPI Middleware & Guard Layers            │
       │    (Cors, Security Headers, Redis Rate Limiter)        │
       └──────────────────────────┬─────────────────────────────┘
                                  │
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │               API Versioned Router (/v1)               │
       │    (Input Validation, Authentication, Route Handlers)   │
       └──────────────────────────┬─────────────────────────────┘
                                  │
         ┌────────────────────────┴────────────────────────┐
         │                                                 │
         ▼                                                 ▼
┌─────────────────────────────────┐               ┌─────────────────────────────────┐
│        Service Layer            │               │      Background Tasks           │
│   (Core Business Logic)         │               │     (Async Workers)             │
└────────┬────────────────┬───────┘               └─────────────────────────────────┘
         │                │
         ▼                ▼
┌─────────────────┐┌───────────────┐
│  Redis Cache    ││ SQLAlchemy ORM│
│ (Session/Tasks) ││ (PyMySQL / DB)│
└─────────────────┘└──────┬────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  MySQL Pool   │
                  └───────────────┘

---

## System Overview

### 1. Authentication & Security Guard
* Token-Based Security: State-of-the-art JWT authentication architecture using python-jose for secure claims serialization.
* Cryptographic Hashing: Salted password hashing via Passlib paired with the bcrypt backend engine.
* Hardened Input Layers: Comprehensive type safety, request schema parsing, and structural data sanitization via Pydantic.

### 2. Performance & Distributed Data
* Asynchronous Engine: Fully non-blocking structural execution paths leveraging Python's native asyncio paradigm.
* Distributed Caching: Intelligent read/write cache management using Redis to intercept hot database queries, reducing structural latency.
* Queue Offloading: Lightweight asynchronous background workers processing continuous non-blocking system tasks out-of-band.

### 3. Observability & Telemetry
* Metrics Collection: Structured system instrumentation reporting runtime resource allocations, latency tracking, and request throughput.
* Health Subsystem: Active operational liveness and readiness API probes assessing structural dependencies (MySQL, Redis).

### 4. Continuous Integration & Infrastructure
* Deterministic Environments: Multistage containerization via Docker ensuring unified localized runs and staging equivalence.
* CI Pipeline Automation: GitHub Actions infrastructure spinning up live isolated services, processing schema migrations, and executing test assertions per commit.

---

## API Structure & Versioning

The API adheres strictly to REST principles and scales via explicitly versioned endpoints under /api/v1.

### Endpoints Matrix

| Domain | Route | HTTP Method | Auth Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| System | /api/v1/health | GET | No | Health check for database and Redis |
| | /api/v1/metrics | GET | No | Basic runtime metrics (uptime, request count) |
| Auth | /api/v1/auth/register | POST | No | Registers a new system identity |
| | /api/v1/auth/login | POST | No | Authorizes user, returns Access JWT |
| Tasks | /api/v1/tasks | GET | Yes | Retrieves paginated user-owned tasks |
| | /api/v1/tasks | POST | Yes | Instantiates a new managed task |
| | /api/v1/tasks/{id} | GET | Yes | Fetches a target task with strict ownership checks |
| | /api/v1/tasks/{id} | PUT | Yes | Updates task specifications |
| | /api/v1/tasks/{id} | DELETE | Yes | Atomically drops a targeted task resource |

---

## Project Directory Layout

task-manager-api/
├── .github/workflows/    # CI Pipeline Orchestration
│   └── ci.yml
├── alembic/              # Declarative Database Migrations Engine
├── app/                  # Application Core Module
│   ├── core/             # System Configuration & Cryptographic Secrets
│   ├── middleware/       # Telemetry Logs, Security Headers & Rate Limiters
│   ├── models/           # Declarative SQLAlchemy Structural Schema Definitions
│   ├── routes/           # Versioned API Router Modules (/v1)
│   ├── schemas/          # Pydantic Structural Request/Response Definitions
│   ├── services/         # Layered Core Business Logic & Cache Layer Interface
│   └── main.py           # Application Bootstrap Engine
├── docs/                 # OpenAPI & Internal Architecture Documentation
├── tests/                # Deterministic Pytest Automation Suite
├── Dockerfile            # Multi-stage Optimized Application Container
├── docker-compose.yml    # Full-Stack Local Infrastructure Blueprint
├── alembic.ini           # Database Migration Mapping Specifications
└── requirements.txt      # Locked External Software Dependencies

---

## DevOps, Infrastructure & CI/CD

This architecture relies heavily on automated verification to enforce stability before merging changes into production.

### GitHub Actions CI Workflow (.github/workflows/ci.yml)
On every pull request or direct push to the main branch, the infrastructure engine performs the following actions inside a clean workflow container:
1. Spins up a native MySQL service container.
2. Automatically maps and runs modern stateful schema files using Alembic.
3. Dispatches the full test runner framework via Pytest to run automated tests covering core application flows

---W

## Local Infrastructure Setup

### Prerequisites
* Python 3.11+
* Docker & Docker Compose

### Native Setup
1. Clone and Navigate:
   git clone <repository-url>
   cd task-manager-api

2. Isolate Environment:
   * Linux/Mac:
     python -m venv venv && source venv/bin/activate
   * Windows:
     python -m venv venv && venv\Scripts\activate

3. Hydrate Dependencies:
   pip install -r requirements.txt

4. Environment Generation:
   cp .env.example .env

5. Run DB Migrations:
   alembic upgrade head

6. Initiate Server:
   uvicorn app.main:app --reload

### Docker-Native Quickstart
To bring up the entire multi-container topology (FastAPI App, MySQL Instance, Redis Caching node) instantly:
docker compose up --build

---

## Example Metrics Response

When querying the live /metrics endpoint, the platform yields comprehensive diagnostic JSON outputs to facilitate clean system alerting:

{
  "status": "healthy",
  "uptime_seconds": 86400,
  "requests_total": 45120,
  "database": "up",
  "redis": "up"
}

---

## System Engineering Competencies Gained

Through developing this production-oriented system, deep engineering expertise was built across the following architectural domains:

* Advanced Scalable Web Design: Implementing performant concurrency abstractions via Python async/await syntax and designing resource-efficient ASGI lifecycles.
* Stateful Database Engineering: Configuring object-relational mapping patterns securely, managing connection pooling mechanisms, and handling programmatic database modifications using declarative Alembic scripts.
* Distributed Strategy Implementation: Integrating high-performance in-memory cache networks utilizing Redis to execute atomic data actions, limit transaction rates, and minimize core compute overhead.
* Modern Site Reliability Engineering (SRE): Formulating end-to-end continuous orchestration systems, instrumenting comprehensive telemetry APIs, and managing isolated container layers.

---

## Live Deployement
 - API: https://task-manager-api-cvf6.onrender.com/
 - DOCS: https://task-manager-api-cvf6.onrender.com/docs
--
## License

Distributed under the MIT Software License. Review the explicit LICENSE asset for terms of use.
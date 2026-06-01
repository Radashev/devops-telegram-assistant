# Architecture Documentation

## 1. System Overview

DevOps Telegram Assistant is a production-oriented Telegram assistant platform.

The system combines:

* Telegram bot interface
* FastAPI backend API
* PostgreSQL database
* background reminder scheduler
* Docker-based runtime
* GitHub Actions CI/CD
* Fly.io cloud deployment

The main goal of the project is to demonstrate a real backend + DevOps workflow: from local development to automated production deployment.

---

## 2. High-Level Architecture

```text
   Telegram User
        ↓
   Aiogram Bot
        ↓
   FastAPI API
        ↓
   PostgreSQL Database

   GitHub Actions
        ↓
   Fly.io Deployment
```

---

## 3. Runtime Components

### API Process

The `api` process runs the FastAPI application with Uvicorn.

Responsibilities:

* expose HTTP API endpoints
* handle `/health` checks
* process users, tasks and reminders
* communicate with PostgreSQL
* run Alembic migrations during container startup

### Bot Process

The `bot` process runs the Aiogram Telegram bot.

Responsibilities:

* receive Telegram commands
* communicate with the FastAPI API
* process user actions
* run background reminder scheduler

### PostgreSQL Database

PostgreSQL stores application data:

* users
* tasks
* reminders

The application uses async SQLAlchemy and asyncpg for database communication.

---

## 4. Functional Modules

The application consists of several functional modules.

### Task Management

Responsible for managing user tasks.

Supported commands:

- `/add`
- `/list`
- `/done`
- `/delete`

Features:

- create tasks
- view tasks
- complete tasks
- delete tasks

---

### Reminder System

Provides recurring monthly reminders.

Supported commands:

- `/remind_monthly`
- `/reminders`
- `/delete_reminder`

Features:

- reminders on a specific day
- reminders on the last day of the month
- background scheduler processing

---

### Google Calendar Integration

Creates events directly in Google Calendar.

Supported command:

- `/gcal`

Features:

- create calendar events
- Google Calendar synchronization

---

### AI Task Planner

Uses AI to generate action plans.

Supported command:

- `/plan_tasks`

Features:

- goal decomposition
- task generation
- productivity assistance

---

### Gmail Assistant

Provides Gmail analysis and automation.

Supported commands:

- `/check_emails`
- `/triage_email`
- `/triage_batch`
- `/archive_preview`

Features:

- inbox analysis
- email categorization
- archive recommendations
- AI-assisted email processing


## 5. Application Layers

```text
app/
├── api/             # FastAPI routes
├── bot/             # Telegram bot handlers and schedulers
├── core/            # configuration
├── db/              # database connection
├── models/          # SQLAlchemy models
├── repositories/    # database access layer
├── schemas/         # Pydantic schemas
├── services/        # business services
├── usecases/        # use case logic
```

### API Layer

Contains FastAPI routers and HTTP endpoints.

### Bot Layer

Contains Telegram bot handlers and scheduler logic.

### Repository Layer

Responsible for database queries and persistence.

### Service Layer

Contains business operations and integrations.

### Use Case Layer

Coordinates business actions between API, services and repositories.

---

## 6. Local Development Architecture

Local development is based on Docker Compose.

```text
Docker Compose
├── api
├── bot
└── postgres
```

Startup flow:

```text
postgres starts
        ↓
api waits for database
        ↓
alembic migrations run
        ↓
FastAPI starts
        ↓
bot starts and connects to API
```

Local healthcheck:

```bash
curl http://localhost:8001/health
```

Expected response:

```json
{"status":"ok"}
```

---

## 7. Production Deployment Architecture

Production deployment is hosted on Fly.io.

```text
GitHub main branch
        ↓
GitHub Actions
        ↓
Fly.io Deploy
        ↓
api process + bot process
```

Production endpoint:

```bash
curl https://devops-telegram-assistant.fly.dev/health
```

Expected response:

```json
{"status":"ok"}
```

---

## 8. CI/CD Flow

### CI

CI runs on push and pull requests.

It checks:

* repository checkout
* Python setup
* Poetry installation
* dependency installation
* API entrypoint compilation
* bot entrypoint compilation
* automated tests
* Docker image build

### CD

CD runs after changes are merged into `main`.

Deployment flow:

```text
merge to main
        ↓
GitHub Actions starts Fly Deploy workflow
        ↓
flyctl deploy --remote-only
        ↓
Fly.io updates machines
        ↓
production healthcheck runs
        ↓
/health must return {"status":"ok"}
```

---

## 9. Git Branching Strategy

The project uses feature-based Git workflow.

```text
main
├── develop
└── feature/*
```

Typical workflow:

```text
create feature branch
        ↓
make changes
        ↓
commit
        ↓
push
        ↓
open pull request
        ↓
CI checks
        ↓
merge
        ↓
deployment
```

---

## 10. Cost Optimization Strategy

The project is designed with low-cost deployment in mind.

Fly.io machines can be scaled manually:

```bash
flyctl scale count api=1
flyctl scale count bot=1
```

To stop machines and reduce runtime cost:

```bash
flyctl scale count api=0
flyctl scale count bot=0
```

The current deployment is optimized for learning, portfolio and MVP usage.

---

## 11. Current Limitations

Current limitations:

* no advanced monitoring yet
* no Terraform infrastructure yet
* no custom domain yet
* database backup strategy still needs improvement
* production logging requires cleanup and optimization

---

## 12. Planned Improvements

Planned architecture improvements:

* Terraform infrastructure
* monitoring with Prometheus and Grafana
* centralized logging
* backup strategy for PostgreSQL
* custom domain
* AWS deployment option
* improved secrets management
* production alerting

---

## 13. Summary

This project demonstrates a complete backend + DevOps lifecycle:

```text
code
↓
Docker
↓
CI
↓
CD
↓
cloud deployment
↓
healthcheck
↓
logs
↓
cost control
```

The architecture is intentionally simple, practical and production-oriented.

# 🚀 DevOps Telegram Assistant

Production-oriented Telegram assistant platform built with **FastAPI, Aiogram, PostgreSQL, Docker, and GitHub Actions CI/CD**.

This project demonstrates a real-world backend + DevOps workflow including:

* asynchronous backend architecture
* Telegram bot integration
* Dockerized services
* database migrations
* CI/CD automation
* cloud deployment on Fly.io
* production healthchecks
* Git branching workflow
* cost-optimized cloud infrastructure

---

# 🧠 Architecture Overview

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
   Fly.io Deploy
```

---

# ⚙️ Tech Stack

## Backend

* Python 3.11
* FastAPI
* Aiogram 3
* SQLAlchemy (async)
* Alembic
* Pydantic

## Database

* PostgreSQL
* asyncpg

## DevOps & Infrastructure

* Docker
* Docker Compose
* GitHub Actions (CI)
* GitHub Actions (CD)
* Fly.io
* Healthchecks
* Cloud logging
* Poetry

## Planned Infrastructure

* AWS (EC2 / ECS / S3 / RDS)
* Terraform
* Monitoring (Prometheus / Grafana)

---

# ✅ Current Features

## Backend

* Async FastAPI application
* REST API endpoints
* `/health` production endpoint
* SQLAlchemy async database layer
* Alembic migrations
* Repository pattern
* Service layer
* Use case layer

## Telegram Bot

* Aiogram-based bot
* Reminder scheduler
* Task management
* Email-related handlers
* Calendar integration

## DevOps

* Dockerized multi-service architecture
* Production-ready Docker setup
* CI pipeline with GitHub Actions
* CD pipeline with Fly.io deployment
* Automatic production healthcheck
* Cloud deployment with process separation (`api` + `bot`)
* Cost-optimized deployment strategy
* Feature branching Git workflow

---

# 🗄 Database Migrations

Alembic is configured for asynchronous SQLAlchemy migrations.

## Create migration

```bash
docker compose exec api poetry run alembic revision --autogenerate -m "message"
```

## Apply migrations

```bash
docker compose exec api poetry run alembic upgrade head
```

---

# 🧱 Project Structure

```text
app/
├── api/             # FastAPI routes
├── bot/             # Telegram bot logic
├── core/            # Configuration and settings
├── db/              # Database connections
├── models/          # SQLAlchemy models
├── repositories/    # Data access layer
├── schemas/         # Pydantic schemas
├── services/        # Service layer
├── usecases/        # Business logic
```

---

# 🐳 Local Development

## Run locally

```bash
docker compose up --build -d
```

## Check containers

```bash
docker compose ps
```

## API healthcheck

```bash
curl http://localhost:8001/health
```

---

# 🚀 Production Deployment

Deployment flow:

```text
feature/* → develop → main → GitHub Actions → Fly.io
```

Production includes:

* automatic deployment after merge to `main`
* production healthcheck validation
* Dockerized cloud deployment
* cloud logging
* API and bot process separation

## Production health endpoint

```bash
curl https://devops-telegram-assistant.fly.dev/health
```

---

# ⚙️ Environment Variables

Example `.env`:

```env
BOT_TOKEN=your_token

DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/db

APP_ENV=development
LOG_LEVEL=INFO
```

---

# 🧪 CI/CD Pipeline

## CI

GitHub Actions automatically:

* install dependencies
* run tests
* validate Python entrypoints
* build Docker image

## CD

After merge into `main`:

* Fly.io deployment starts automatically
* production machine updates
* production healthcheck validates deployment

---

# 📌 Roadmap

## Backend

* advanced task management
* notes system
* user authentication
* background jobs

## DevOps

* Terraform infrastructure
* monitoring and metrics
* centralized logging
* AWS production deployment

---

# 💡 Author

**Vasyl Radashev**

Backend / DevOps Engineer focused on production-ready systems, CI/CD automation, Dockerized infrastructure and cloud deployment.

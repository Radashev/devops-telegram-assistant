🚀 DevOps Telegram Assistant

A production-oriented Telegram assistant built with FastAPI, Aiogram, PostgreSQL, MongoDB, and Docker.

This project demonstrates a real-world backend + DevOps architecture, evolving from a local bot into a cloud-ready system.

🧠 Architecture Overview
Telegram → Aiogram Bot → Use Cases → Repositories → Database
                                ↙
                          FastAPI API
⚙️ Tech Stack
Current stack

Python 3.11

FastAPI

Aiogram 3

PostgreSQL

MongoDB

Docker & Docker Compose

Poetry

Planned DevOps / Cloud stack

Fly.io

AWS (EC2 / ECS / S3 / RDS)

GitHub Actions (CI/CD)

Terraform (Infrastructure as Code)

⚙️ Features
🤖 Bot Core

/start — initialize user, sync with database

/ping — check MongoDB and PostgreSQL connectivity

/whoami — display Telegram user data

🗃 Task Management

/add_task <text> — create a task

/tasks — list saved tasks

🌍 Translation

/tr <text> — translate UA ↔ EN

auto-translation for regular messages

🤖 AI Assistant

/gpt <question> — GPT-based responses

⏰ Reminders

Flexible reminder system:

exact datetime

relative time

natural language

Examples:

/remind 2026-01-07 20:40 Go outside
/remind через 5 хвилин зробити паузу
/remind tomorrow at 09:00 send CV
📅 Google Integration

/gcal — create Google Calendar event

/note — save notes to Google Drive

🎙 Voice Processing

voice → text (speech recognition)

foundation for voice command system

🧱 Project Structure
app/
  api/            # FastAPI routes
  bot/            # Telegram bot logic
  core/           # config, security
  db/             # database connections
  models/         # ORM models
  repositories/   # data access layer
  schemas/        # Pydantic schemas
  usecases/       # business logic
🐳 Local Development

Run the project locally:

docker-compose up --build

Health check:

curl http://localhost:8000/health
⚙️ Environment Variables

Example .env:

DATABASE_URL=postgresql+asyncpg://...
MONGO_URL=...
BOT_TOKEN=...
🚧 In Progress

SQLAlchemy async integration

repository pattern (PostgreSQL)

Alembic migrations

clean architecture refactoring

API ↔ bot integration

🎯 Roadmap
Phase 1 — Backend Foundation

 PostgreSQL models

 async SQLAlchemy setup

 repository layer

 use cases

Phase 2 — Production Readiness

 Docker multi-service setup

 environment separation (dev/prod)

 logging & monitoring

Phase 3 — CI/CD

 GitHub Actions pipelines

 Docker image build & push

 automated deployment

Phase 4 — Cloud Deployment

 Fly.io deployment (MVP)

 AWS deployment (production)

 domain + HTTPS

 managed databases (RDS)

Phase 5 — Advanced DevOps

 Terraform infrastructure

 observability (Prometheus/Grafana)

 scaling bot workers

 background jobs & queues

🎯 Goal

The goal of this project is to evolve into a production-grade AI assistant platform and demonstrate real-world DevOps and backend engineering skills:

clean architecture

scalable system design

infrastructure thinking

automation mindset

💡 Author

Vasyl Radashev
DevOps / Backend Engineer (in progress 🚀)
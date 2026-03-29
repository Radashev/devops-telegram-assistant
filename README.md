# 🚀 DevOps Telegram Assistant

A production-oriented Telegram assistant built with **FastAPI, Aiogram, PostgreSQL, MongoDB, and Docker**.

This project demonstrates a **real-world backend + DevOps architecture**, evolving from a simple bot into a scalable, cloud-ready system.

---

## 🧠 Architecture Overview

```
Telegram → Aiogram Bot → Use Cases → Repositories → Database
                          ↘ FastAPI API
```

---

## ⚙️ Tech Stack

### Backend

* Python 3.11
* FastAPI
* Aiogram 3
* SQLAlchemy (async)
* Alembic (migrations)

### Databases

* PostgreSQL
* MongoDB

### DevOps

* Docker & Docker Compose
* Poetry
* Git (feature branching)

### Planned

* Fly.io
* AWS (EC2 / ECS / S3 / RDS)
* GitHub Actions (CI/CD)
* Terraform

---

## ✅ Current Status

### Implemented

* Clean Git workflow (`main`, `develop`, `feature/*`)
* Python 3.11.5 managed with Poetry
* Dockerized application (multi-service)
* FastAPI app with `/health` endpoint
* Aiogram bot with basic commands (`/start`)
* PostgreSQL (async SQLAlchemy)
* MongoDB integration
* User model with persistence
* API endpoints:

  * `GET /users`
  * `GET /users/{id}`

---

## 🗄 Database Migrations (Alembic)

* Alembic configured for async SQLAlchemy
* Initial migration created for `users` table
* Schema evolution supported

### Commands

```bash
docker-compose exec api poetry run alembic revision --autogenerate -m "message"
docker-compose exec api poetry run alembic upgrade head
```

---

## 🧱 Project Structure

```
app/
├── api/           # FastAPI routes
├── bot/           # Telegram bot logic
├── core/          # config, settings, security
├── db/            # database connections
├── models/        # ORM models
├── repositories/  # data access layer
├── schemas/       # Pydantic schemas
├── usecases/      # business logic
```

---

## 🐳 Local Development

Run project:

```bash
docker-compose up --build
```

Health check:

```bash
curl http://localhost:8000/health
```

---

## ⚙️ Environment Variables

Example `.env`:

```env
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/db
MONGO_URL=mongodb://mongo:27017
BOT_TOKEN=your_token
```

---

## 🚧 In Progress

* Repository pattern (PostgreSQL)
* Clean architecture refactoring
* API ↔ bot integration

---

## 📌 Next Steps

* Task model with foreign key to users
* Task API endpoints
* Reminder system
* Notes system

---

## 🎯 Roadmap

### Phase 1 — Backend Foundation

* PostgreSQL models
* async SQLAlchemy
* repository layer
* use cases

### Phase 2 — Production Readiness

* environment separation (dev/prod)
* logging & monitoring

### Phase 3 — CI/CD

* GitHub Actions pipelines
* Docker build & push

### Phase 4 — Cloud Deployment

* Fly.io (MVP)
* AWS (production)
* domain + HTTPS

### Phase 5 — Advanced DevOps

* Terraform
* monitoring (Prometheus/Grafana)
* background jobs & queues

---

## 💡 Author

**Vasyl Radashev**
DevOps / Backend Engineer (in progress 🚀)


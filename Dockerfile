FROM python:3.11-slim

# Real-time logs
ENV PYTHONUNBUFFERED=1

# Disable .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Project root
ENV PYTHONPATH=/app

WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install Poetry and dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev libpq-dev \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --only main \
    && pip cache purge \
    && apt-get purge -y --auto-remove gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо весь проект
COPY . .

EXPOSE 8000

# Запускаємо як модуль
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
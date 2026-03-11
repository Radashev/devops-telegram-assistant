FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . .

CMD ["python", "app/main.py"]
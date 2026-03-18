FROM python:3.11-slim

# Встановлюємо змімінну середовища, щоб бачити логи в реальному часі
ENV PYTHONUNBUFFERED=1
# Додаємо корінь проекту до шляху пошуку модулів
ENV PYTHONPATH=/app

WORKDIR /app

# Копіюємо конфіги Poetry
COPY pyproject.toml poetry.lock* ./

# Встановлюємо poetry та залежності
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --only main

# Копіюємо весь проект
COPY . .

# Запускаємо як модуль
CMD ["python", "-m", "app.bot.main"]
FROM python:3.12-slim

# Встановлюємо системні залежності
RUN apt-get update && apt-get install -y \
    ffmpeg \
    flac \
    git \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо poetry
RUN pip install --no-cache-dir poetry

# Встановлюємо робочий каталог
WORKDIR /app

# Копіюємо pyproject.toml і poetry.lock для установки залежностей
COPY pyproject.toml poetry.lock /app/

# Встановлюємо залежності проекту
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копіюємо решту файлів проекту
COPY . /app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
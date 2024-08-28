# Stage 1: Build
FROM python:3.11-slim AS builder

# Встановлюємо змінні оточення
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Встановлюємо необхідні пакети
RUN apt-get update \
    && apt-get install -y \
    build-essential \
    libpq-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо робочий каталог
WORKDIR /app

# Копіюємо файл залежностей
COPY requirements.txt /app/

# Встановлюємо залежності
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Stage 2: Final
FROM python:3.11-slim

# Встановлюємо змінні оточення
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Встановлюємо необхідні пакети
RUN apt-get update \
    && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо робочий каталог
WORKDIR /app

# Копіюємо залежності з етапу зборки
COPY --from=builder /usr/local /usr/local

# Копіюємо весь вихідний код в контейнер
COPY . /app/

# Вказуємо порт
EXPOSE 8001

# Команда для запуску програми з параметром таймауту воркерів
CMD ["gunicorn", "--worker-class", "gevent", "root.wsgi:application", "--bind", "0.0.0.0:8001", "--timeout", "300"]

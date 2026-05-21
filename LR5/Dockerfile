FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Установка системных зависимостей (для Pillow, psycopg2 и др.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование и установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Сбор статики (WhiteNoise)
RUN python manage.py collectstatic --noinput

# Запуск через Gunicorn (вместо runserver)
CMD ["sh", "-c", "python manage.py migrate && gunicorn LR5.wsgi:application --bind 0.0.0.0:$PORT"]
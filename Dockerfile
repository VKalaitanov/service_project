FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Устанавливаем обновления и необходимые модули
RUN apk update && \
    apk add --no-cache libpq gcc python3-dev musl-dev postgresql-dev && \
    pip install --upgrade pip

# Установка пакетов для проекта
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

# Копирование проекта
COPY . .

# Настройка записи и доступа (если необходимо)
RUN chmod -R 755 ./

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "service_project.wsgi:application"]

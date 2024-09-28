# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения в контейнер
COPY . .

# Выполняем миграции при старте контейнера
CMD ["python", "manage.py", "migrate"]

# Запускаем приложение с Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "service_project.wsgi:application"]

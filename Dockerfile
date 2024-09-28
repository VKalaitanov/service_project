# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы требований и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию
COPY . .

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Запускаем Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "service_project.wsgi:application"]

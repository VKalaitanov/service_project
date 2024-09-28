FROM python:3.10-slim

# Устанавливаем переменные окружения для предотвращения создания pyc файлов и буферизации вывода.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаем и устанавливаем рабочую директорию.
WORKDIR /app

# Устанавливаем зависимости.
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект Django в контейнер.
COPY . /app/

# Выполняем миграции и собираем статические файлы.
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Открываем порт, на котором работает приложение Django.
EXPOSE 8000

# Запускаем приложение Django с использованием gunicorn.
CMD ["gunicorn", "service_project.wsgi:application", "--bind", "0.0.0.0:8000"]

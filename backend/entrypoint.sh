#!/bin/bash
set -e

echo "=== Применяем миграции ==="
python manage.py migrate --noinput

echo "=== Собираем статику ==="
python manage.py collectstatic --noinput

echo "=== Загружаем ингредиенты ==="
python manage.py load_ingredients

echo "=== Создаём суперпользователя ==="
python manage.py shell << END
from django.contrib.auth import get_user_model
import os

User = get_user_model()
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@foodgram.ru')
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        username=username,
        first_name='Admin',
        last_name='Adminov',
        password=password
    )
    print(f'Суперпользователь {email} создан')
else:
    print(f'Суперпользователь {email} уже существует')
END

echo "=== Создаём тестовые данные ==="
python manage.py create_test_data

echo "=== Запускаем Gunicorn ==="
gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 --workers 3 --access-logfile -
# Foodgram — сервис публикации рецептов

Foodgram — это веб-приложение, где пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное, подписываться на авторов и формировать список покупок.

## 🚀 Работающий сайт

Проект доступен по адресу:

**[http://158.160.230.31/](http://158.160.230.31/)**

## 📋 Возможности проекта

- **Просмотр рецептов** — главная страница с пагинацией, сортировка по дате
- **Регистрация и авторизация** — создание аккаунта, вход по email и паролю
- **Создание рецептов** — добавление своих рецептов с фото, ингредиентами и тегами
- **Избранное** — добавление понравившихся рецептов в избранное
- **Список покупок** — формирование списка ингредиентов и скачивание файлом
- **Подписки** — подписка на авторов и просмотр их рецептов
- **Фильтрация по тегам** — поиск рецептов по тегам
- **Короткие ссылки** — возможность поделиться ссылкой на рецепт
- **Админ-панель** — управление контентом через Django Admin

## 🛠️ Технологии

- **Backend:** Python 3.11, Django 4.2, Django REST Framework, Djoser
- **Frontend:** React (SPA)
- **База данных:** PostgreSQL (продакшен), SQLite (разработка)
- **Веб-сервер:** Nginx
- **Контейнеризация:** Docker, Docker Compose
- **CI/CD:** GitHub Actions

## 📦 Установка и запуск

### Локальная разработка (бэкенд)

1. Клонируйте репозиторий:
```bash
git clone https://github.com/VladTheDevolper/foodgram.git
cd foodgram/backend/
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Примените миграции:
```bash
python manage.py migrate
```

4. Загрузите ингредиенты:
```bash
python manage.py load_ingredients
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

6. Запустите сервер:
```bash
python manage.py runserver
```

Бэкенд доступен по адресу: `http://127.0.0.1:8000/`

### Запуск в Docker (продакшен)

1. Создайте файл `.env` в корне проекта:
```
SECRET_KEY=ваш_секретный_ключ
DEBUG=False
ALLOWED_HOSTS=ваш_ip,localhost,127.0.0.1
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=ваш_пароль
DB_HOST=db
DB_PORT=5432
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@foodgram.ru
DJANGO_SUPERUSER_PASSWORD=ваш_пароль_админа
```

2. Запустите контейнеры:
```bash
cd infra/
docker compose up -d --build
```

Приложение доступно по адресу: `http://localhost/`

## 📚 Документация API

Документация API доступна по адресу:

`http://158.160.230.31/api/docs/`

## 🔑 Админ-панель

Админ-панель Django доступна по адресу:

`http://158.160.230.31/admin/`

## 📖 Примеры запросов к API

### Регистрация пользователя
```
POST /api/users/
Content-Type: application/json

{
    "email": "user@example.com",
    "username": "username",
    "first_name": "Имя",
    "last_name": "Фамилия",
    "password": "securepassword"
}
```

### Получение токена
```
POST /api/auth/token/login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword"
}
```

### Создание рецепта
```
POST /api/recipes/
Authorization: Token ваш_токен
Content-Type: application/json

{
    "ingredients": [{"id": 1, "amount": 100}],
    "tags": [1, 2],
    "image": "data:image/png;base64,...",
    "name": "Название рецепта",
    "text": "Описание рецепта",
    "cooking_time": 30
}
```

### Получение списка рецептов
```
GET /api/recipes/?tags=breakfast&author=1&page=1&limit=6
```

### Добавление в избранное
```
POST /api/recipes/{id}/favorite/
Authorization: Token ваш_токен
```

### Скачать список покупок
```
GET /api/recipes/download_shopping_cart/
Authorization: Token ваш_токен
```

### Подписка на автора
```
POST /api/users/{id}/subscribe/
Authorization: Token ваш_токен
```

## 👤 Автор

Студент Яндекс.Практикума  
Факультет Бэкенд-разработки

## 📄 Лицензия

MIT License
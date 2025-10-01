# Electronics Network (Django + DRF + PostgreSQL)

Иерархическая сеть по продаже электроники  
(0 — завод, 1 — розничная сеть, 2 — индивидуальный предприниматель)  
с админкой и REST API.

---

## Стек
- Python 3.12
- Django 5, Django REST Framework, django-filter
- PostgreSQL 15+
- pytest, pytest-django (тесты)
- Poetry (управление зависимостями)

---

## Установка и запуск

### 1. Клонирование и окружение
```
git clone <repo_url>
cd electronics_network
poetry install
poetry shell
```

### 2. Настройка PostgreSQL
Создай базу и пользователя в PostgreSQL (в psql или pgAdmin):

CREATE DATABASE electronics;
CREATE USER postgres WITH ENCRYPTED PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE electronics TO postgres;
### 3. Создай файл .env в корне проекта

POSTGRES_DB=electronics
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

DJANGO_DEBUG=True
DJANGO_SECRET_KEY=dev-secret-key
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
### 4. Миграции и суперпользователь
```
python manage.py migrate
python manage.py createsuperuser
```
### 5. (опционально) Демо-данные
```
python manage.py loaddata network/fixtures/seed.json
```
### 6. Запуск сервера
```
python manage.py runserver
```
Админка: http://127.0.0.1:8000/admin/
API: http://127.0.0.1:8000/api/

## API
CRUD для звеньев сети
GET /api/suppliers/ — список
POST /api/suppliers/ — создать
GET /api/suppliers/{id}/ — получить
PATCH /api/suppliers/{id}/ — изменить (поле debt игнорируется)
DELETE /api/suppliers/{id}/ — удалить

Фильтрация
По стране:
/api/suppliers/?country=Georgia

Продукты
GET/POST /api/products/
GET/PUT/PATCH/DELETE /api/products/{id}/

## Доступ и права
Доступ к API только для активных сотрудников (is_active=True, is_staff=True).
Поле debt:
можно указать при создании (POST);
нельзя обновить через API (при PATCH/PUT игнорируется).

## Админка
Вывод списка объектов с фильтрацией по городу и стране.
Ссылка на поставщика внутри карточки.
Admin action: очистка задолженности у выбранных объектов.

## Тесты
```
pytest -q
```
Покрытие тестами:
модели (иерархия, запрет глубины > 2);
admin action «очистить задолженность»;
API (создание, фильтрация, запрет изменения debt);
права доступа (только staff).

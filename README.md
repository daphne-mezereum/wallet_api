# Django REST API (PostgreSQL + Docker)

Backend-проект на **Django** с использованием **Django REST Framework** и базы данных **PostgreSQL**.  
Проект поддерживает локальный запуск и запуск в Docker через `docker-compose`.

Все API-эндпоинты доступны по префиксу **`/api/v1/`**.

---

## Технологии

- Python 3.12  
- Django 6.0.1  
- Django REST Framework 3.16.1  
- PostgreSQL 16  
- psycopg (binary)  
- python-dotenv  
- Docker / Docker Compose  

Все зависимости описаны в `requirements.txt`.

---

### Основные переменные

| Переменная | Описание |
|-----------|----------|
| SECRET_KEY | Секретный ключ Django |
| DEBUG_CONF | Режим отладки (`True` / `False`) |
| HOST | Хост приложения |
| POSTGRES_DB | Имя базы данных |
| POSTGRES_USER | Пользователь PostgreSQL |
| POSTGRES_PASSWORD | Пароль PostgreSQL |
| DATABASE_HOST | Хост базы данных |
| DATABASE_PORT | Порт базы данных |

---

## Файлы конфигурации

- `config.env` — конфигурация для локального запуска  
- `config_exp.env` — пример (шаблон) для `config.env`  
- `config_docker.env` — конфигурация для Docker  
- `config_docker_exp.env` — пример для `config_docker.env`  

---

## Локальный запуск

### 1. Клонирование проекта

```bash
git clone <repo_url>
cd <project_root>
```

### 2. Виртуальное окружение

```bash
python -m venv .venv
```

Активация:

```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Создание `config.env`

```env
SECRET_KEY=django-insecure-change-me
HOST=127.0.0.1
POSTGRES_DB=db
POSTGRES_USER=user
POSTGRES_PASSWORD=12345
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
DEBUG_CONF=True
```

### 5. Применение миграций

```bash
python manage.py migrate
```

### 6. Создание суперпользователя (опционально)

```bash
python manage.py createsuperuser
```

### 7. Запуск сервера

```bash
python manage.py runserver
```

---

## Запуск через Docker

### 1. Подготовка `config_docker.env`

```env
SECRET_KEY=django-insecure-change-me
POSTGRES_DB=db_name
POSTGRES_USER=user_name
POSTGRES_PASSWORD=12345
DATABASE_HOST=db
DATABASE_PORT=5432
DEBUG_CONF=True
```

### 2. Запуск контейнеров

```bash
docker-compose up --build
```

Остановка:

```bash
docker-compose down
```

---

## Миграции

Создание миграций:

```bash
python manage.py makemigrations
```

Применение миграций:

```bash
python manage.py migrate
```

---

## Админка

Административная панель Django:

```
/admin/
```

Для доступа необходим суперпользователь.

---

## Продакшен

Перед деплоем необходимо:

- установить `DEBUG_CONF=False`
- задать безопасный `SECRET_KEY`
- настроить `ALLOWED_HOSTS`
- хранить конфигурацию только в переменных окружения

---

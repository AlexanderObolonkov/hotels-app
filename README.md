# Hotels App

[![Build status](https://github.com/AlexanderObolonkov/hotels-app/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/AlexanderObolonkov/hotels-app/actions/workflows/checks.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Стек:
- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Celery
- Pytest
- Prometheus
- Grafana
- Docker
- GitHub Actions & Pre-commit

## Запуск

Скопируйте `.env.example`
1) без Docker в `.env`,
2) с Docker в `.env-non-dev`,

заполнив в нём все переменные окружения

```bash
cp .env.example .env.  # env-non-dev
```

Для управления зависимостями используется poetry, требуется Python 3.11.

- Без контейнеризации

```bash
poetry install
poetry shell
alembic upgrade head
uvicorn app.main:app
celery -A app.tasks.celery:celery worker --loglevel=INFO
```

- С помощью Docker Compose

```bash
docker compose build
docker compose up
```

## Ideas
- Добавить логику при приближении бронирования
- Расширить логику с пользователями, добавить роли
- Добавить отзывы
# PopScope 📊

Аналитическая платформа для анализа демографических данных муниципальных образований России с прогнозированием тенденций.

## 🚀 Быстрый старт

**👉 [Читайте полное руководство по запуску](SETUP.md)**

Минимум для локального запуска:

```bash
# 1. Клонируйте проект
git clone <repository-url>
cd PopScope

# 2. Запустите все сервисы (требуется Docker)
docker compose up -d

# 3. Откройте в браузере
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/docs
```

## 📋 Что включено

- ✅ **FastAPI Backend** — RESTful API с асинхронной обработкой
- ✅ **React Frontend** — UI с аналитическими графиками и 
- ✅ **PostgreSQL** — реляционная БД для хранения данных
- ✅ **Alembic** — управление миграциями БД
- ✅ **Docker Compose** — одноконтейнерное развертывание
- ✅ **Pytest** — полное покрытие тестами
- ✅ **LLM Integration** — опциональная интеграция с Yandex GPT для отчетов
- ✅ **Seeds** — автоматическая загрузка демографических данных при старте

## 🏗️ Архитектура

```
Frontend (React + Vite)         Backend (FastAPI)           Database (PostgreSQL)
    :5173                           :8000                         :5433
```

## 📚 Основные разделы

- **[Гайд по запуску](SETUP.md)** — Подробные инструкции для новых разработчиков
- **[API документация](http://localhost:8000/docs)** — Swagger UI (после запуска)
- **Backend:** `backend/app/` — Основной код приложения
- **Frontend:** `frontend/src/` — React компоненты и страницы

## 🧪 Разработка и тестирование

```bash
# Запустите тесты
docker compose exec backend pytest

# Просмотрите покрытие
docker compose exec backend pytest --cov
```

## ⚙️ Переменные окружения

Основные параметры в `.env`:
- `POSTGRES_PASSWORD` — пароль БД
- `APP_ENV` — режим (dev/prod)
- `REPORT_USE_LLM` — использовать ли LLM для отчетов
- `YANDEX_GPT_*` — параметры Yandex GPT (если LLM включен)

## 📖 Дополнительно

- Все компоненты Radix UI используют Tailwind CSS
- Графики и визуализация с помощью Material-UI и Leaflet
- Полная типизация Python (Pydantic) и TypeScript

---

**PopScope** © 2026 — Платформа аналитики населения

# 📝 Быстрая шпаргалка по PopScope

## 1️⃣ Первый запуск

```bash
git clone <repository-url>
cd PopScope

# Backend + БД (Docker должен быть скачан и открыт)
docker compose up -d (если нужен не демон, то уберите -d)

# Frontend (в отдельном терминале)
cd frontend
npm install
npm run dev
```

✅ **Готово!** Проект запущен:
- Frontend: http://localhost:5173
- API: http://localhost:8000\

---

## 🔗 Полезные ссылки

| Компонент | URL | Что это |
|-----------|-----|--------|
| Frontend | http://localhost:5173 | Основное приложение |
| API Docs | http://localhost:8000/docs | Swagger интерфейс |
| ReDoc | http://localhost:8000/redoc | Документация API |
| Database | localhost:5433 | PostgreSQL (если нужен прямой доступ) |

---

## 🛠️ Частые команды

```bash
# Смотреть логи
docker compose logs -f backend

# Запустить тесты
docker compose exec backend pytest

# Войти в контейнер
docker compose exec backend bash

# Перезагрузить
docker compose restart

# Остановить все
docker compose down

# Полный сброс (данные БД будут восстановлены автоматически при следующем запуске)
docker compose down -v && docker compose up -d
```

---

## 🔑 Важно запомнить

- **БД пароль:** `dunduk10` (в файле `.env`)
- **Порт backend:** `8000`
- **Порт frontend:** `5173`
- **Порт БД:** `5433`

Если порты заняты, измените в `.env`

---

## 📂 Структура кода

```
backend/     → FastAPI, БД, API endpoints
frontend/    → React, UI компоненты
db/          → SQL инициализация
```

---

## ❌ Что-то не работает?

1. **Проверьте контейнеры:**
   ```bash
   docker compose ps
   ```

2. **Смотрите ошибки:**
   ```bash
   docker compose logs backend
   docker compose logs db
   ```

3. **Сбросьте всё:**
   ```bash
   docker compose down -v
   docker compose up -d
   ```

👉 Полная документация: [SETUP.md](SETUP.md)

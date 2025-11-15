# Право выбора — ChatBot (MAX)

## Кратко

Чат-бот «Право выбора» — цифровой помощник для людей, возвращающихся к нормальной жизни после сложных обстоятельств. Помогает восстановить документы, найти программы поддержки и работу, получить первую психологическую помощь и связаться с профильными НКО. Команда Ганшина Ярослава.

## Состав проекта

- backend/ — FastAPI-приложение (API + DB seed)
- infra/partners.csv — пример базы НКО/партнёров
- bot_flow.json — flow для конструктора бота

## Требования

- Python 3.11+
- Docker & Docker Compose (опционально)
- VS Code (рекомендовано)
- MAX bot token (получается у организаторов)

## Переменные окружения

Скопируйте `.env.example` → `.env` и заполните значения (особенно `MAX_TOKEN`, `DATABASE_URL`, `ADMIN_SECRET`, `SECRET_KEY`).

## Как запустить (локально, без Docker)

1. Откройте проект в VS Code.

2. Создайте виртуальное окружение:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate      # Windows (PowerShell)
   ```

3. Установите зависимости:

   ```bash
   pip install -r backend/requirements.txt
   ```

4. Настройте `.env`:
   
   Создайте файл `.env` в корне проекта и скопируйте туда содержимое из `.env.example`, затем заполните реальные значения:
   - `MAX_TOKEN` — токен от MAX (не публикуйте!)
   - `DATABASE_URL` — для локального запуска: `postgresql+asyncpg://postgres:postgres@localhost:5432/right_to_choice`
   - `ADMIN_SECRET` — любой секретный ключ для админ-API
   - `SECRET_KEY` — случайная строка для шифрования

5. Создайте таблицы:

   ```bash
   python backend/create_tables.py
   ```

6. Заполните партнёров:

   ```bash
   python backend/seed_partners.py
   ```

7. Запустите приложение:

   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

8. Документация OpenAPI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Как запустить через Docker

### Быстрый запуск (рекомендуется)

1. **Создайте `.env` файл** в корне проекта:
   ```bash
   cp .env.example .env
   ```
   Заполните значения (особенно `MAX_TOKEN`, `DATABASE_URL`).

2. **Соберите и запустите контейнеры:**
   ```bash
   docker compose up --build
   ```

3. **В отдельном терминале создайте таблицы и загрузите данные:**
   ```bash
   docker exec -it right_to_choice_backend_1 python create_tables.py
   docker exec -it right_to_choice_backend_1 python seed_partners.py
   ```

4. **Проверьте работу:**
   - API документация: http://localhost:8000/docs
   - Webhook endpoint: http://localhost:8000/webhook

### Альтернативный запуск (одной командой)

```bash
# Сборка и запуск
docker compose up --build -d

# Ожидание запуска БД (5 секунд)
sleep 5

# Создание таблиц и загрузка данных
docker exec right_to_choice_backend_1 python create_tables.py
docker exec right_to_choice_backend_1 python seed_partners.py

# Проверка логов
docker compose logs -f backend
```

### Остановка

```bash
docker compose down
```

### Очистка (удаление данных)

```bash
docker compose down -v
```

## Тестовый запрос (curl)

```bash
curl -X POST "http://localhost:8000/api/requests" \
  -H "Content-Type: application/json" \
  -d '{"category":"Восстановить документы","region":"Москва","short_text":"Потерян паспорт","phone":"+7-999-000-00-00","consent":true}'
```

## Безопасность / PII

* В продакшене телефон и другие PII шифруются и хранятся минимально.


## Интеграция с MAX Platform

Проект готов к работе с MAX Platform. Токен уже настроен в `.env`.

### Основные возможности:

- ✅ Webhook handler для приёма сообщений от MAX
- ✅ Отправка сообщений пользователям через MAX API
- ✅ Обработка кнопок и текстовых сообщений
- ✅ Интеграция с базой данных для сохранения заявок

## Контакты команды

Email: 54321yaroslav@mail.ru  
Телефон: +79119995057

Подробная информация: см. [CONTACTS.md](CONTACTS.md)


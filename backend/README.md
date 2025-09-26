# Freelance Market API

Базовый API для freelance биржи в Telegram Mini Apps с микросервисной архитектурой.

## Архитектура

Проект построен на микросервисной архитектуре с разделением на следующие сервисы:

- **User Service** - управление пользователями и аутентификация
- **Order Service** - управление заказами
- **Skill Service** - управление навыками и категориями
- **Proposal Service** - управление предложениями фрилансеров
- **Notification Service** - система уведомлений
- **Search Service** - поиск и фильтрация
- **Analytics Service** - аналитика и статистика

## Технологии

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM для работы с базой данных
- **Pydantic** - валидация данных
- **aiogram** - Telegram Bot API
- **JWT** - аутентификация

## Установка и запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл `.env` с настройками:
```env
BOT_TOKEN=your_telegram_bot_token
WEBHOOK_PATH=/webhook
WEBHOOK_URL=https://your-domain.com/webhook
DEBUG=True
MY_TELEGRAM_TOKEN=your_telegram_token
DATABASE_URL=sqlite+aiosqlite:///./database.db
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_ADAPTER=pyjwt
MOCK_USER=test_user
```

3. Запустите приложение:
```bash
python main.py
```

## API Endpoints

### Пользователи (`/api/users`)
- `POST /` - создание пользователя
- `GET /` - получение всех пользователей
- `GET /{tg_id}` - получение пользователя по Telegram ID
- `PUT /{tg_id}` - обновление пользователя
- `DELETE /{tg_id}` - удаление пользователя
- `POST /login` - аутентификация через Telegram

### Заказы (`/api/orders`)
- `POST /` - создание заказа
- `GET /{order_id}` - получение заказа по ID
- `PUT /{order_id}` - обновление заказа
- `DELETE /{order_id}` - удаление заказа

### Навыки (`/api/skills`)
- `POST /` - создание навыка
- `GET /` - получение всех навыков
- `GET /{skill_id}` - получение навыка по ID
- `PUT /{skill_id}` - обновление навыка
- `DELETE /{skill_id}` - удаление навыка

### Предложения (`/api/proposals`)
- `POST /` - создание предложения
- `GET /` - получение предложений
- `GET /{proposal_id}` - получение предложения по ID
- `PUT /{proposal_id}` - обновление предложения
- `DELETE /{proposal_id}` - удаление предложения
- `POST /{proposal_id}/accept` - принятие предложения
- `POST /{proposal_id}/reject` - отклонение предложения

### Уведомления (`/api/notifications`)
- `POST /` - создание уведомления
- `GET /` - получение уведомлений пользователя
- `GET /{notification_id}` - получение уведомления по ID
- `PUT /{notification_id}/read` - отметка как прочитанное
- `DELETE /{notification_id}` - удаление уведомления

### Поиск (`/api/search`)
- `GET /orders` - поиск заказов
- `GET /freelancers` - поиск фрилансеров
- `GET /suggestions` - получение предложений для поиска

### Аналитика (`/api/analytics`)
- `GET /user/{user_id}/stats` - статистика пользователя
- `GET /orders/stats` - статистика заказов
- `GET /platform/stats` - статистика платформы
- `GET /revenue/stats` - статистика доходов
- `GET /skills/stats` - статистика навыков

## Модели данных

### Пользователь (User)
- `tg_id` - Telegram ID
- `first_name` - имя
- `last_name` - фамилия
- `username` - имя пользователя
- `language_code` - код языка
- `is_premium` - премиум статус
- `allows_write_to_pm` - разрешение писать в ЛС
- `photo_url` - URL фото

### Заказ (Order)
- `uuid` - уникальный идентификатор
- `title` - заголовок
- `description` - описание
- `author_id` - ID автора
- `status` - статус (moderation, active, in_progress, completed, cancelled)
- `primary_responses` - количество откликов
- `created_at` - дата создания
- `updated_at` - дата обновления

### Навык (Skill)
- `id` - идентификатор
- `name` - название
- `description` - описание
- `category` - категория

### Предложение (Proposal)
- `id` - идентификатор
- `order_id` - ID заказа
- `freelancer_id` - ID фрилансера
- `message` - сообщение
- `price` - цена в копейках
- `status` - статус (pending, accepted, rejected)
- `created_at` - дата создания
- `updated_at` - дата обновления

## Аутентификация

API использует JWT токены для аутентификации. Токен получается через endpoint `/api/users/login` с передачей `init_data` от Telegram WebApp.

## CORS

API настроен для работы с фронтендом по адресам:
- `https://freelance-market-chi.vercel.app`
- `http://localhost:8080`

## Разработка

Для разработки используйте:
```bash
uvicorn main:app --reload --host localhost --port 8000
```

API документация доступна по адресу: `http://localhost:8000/docs`

# QR Code Wars

Проект для генерации QR-кодов с мотивационными фразами на немецком языке, отслеживанием прогресса и лидерборда пользователей.

## Структура проекта

- **backend/** - бэкенд на FastAPI с API для генерации QR-кодов и работы с пользователями
- **frontend/** - фронтенд на React для отображения фраз, карты и лидерборда

## Требования

- Python 3.8+
- Node.js 16+
- PostgreSQL

## Установка и запуск

### Настройка базы данных

1. Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE qrcodewars;
```

### Запуск бэкенда

1. Перейдите в директорию backend:

```bash
cd backend
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Настройте переменные окружения:

```bash
# Для Linux/Mac
export DATABASE_URL=postgresql://postgres:postgres@localhost/qrcodewars
export SECRET_KEY=your-secret-key
export QR_SECRET_SALT=your-qr-secret-salt

# Для Windows
set DATABASE_URL=postgresql://postgres:postgres@localhost/qrcodewars
set SECRET_KEY=your-secret-key
set QR_SECRET_SALT=your-qr-secret-salt
```

4. Запустите миграции:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

5. Запустите сервер:

```bash
uvicorn app.main:app --reload
```

Бэкенд запустится по адресу: `http://localhost:8000`

### Запуск фронтенда

1. Перейдите в директорию frontend:

```bash
cd frontend
```

2. Установите зависимости:

```bash
npm install
```

3. Запустите приложение:

```bash
npm start
```

Фронтенд запустится по адресу: `http://localhost:3000`

## API Endpoints

- `GET /api/v1/phrases` - получить список всех фраз
- `GET /api/v1/phrases/{hash}` - получить фразу по хешу
- `POST /api/v1/phrases` - создать новую фразу
- `GET /api/v1/phrases/{phrase_id}/qrcode` - получить QR-код для фразы
- `GET /api/v1/phrases/print/all` - получить PDF со всеми QR-кодами
- `POST /api/v1/users/register` - регистрация нового пользователя
- `POST /api/v1/users/token` - вход пользователя и получение токена
- `GET /api/v1/users/me` - информация о текущем пользователе
- `GET /api/v1/users/leaderboard` - лидерборд пользователей
- `POST /api/v1/users/scan/{phrase_hash}` - отметить QR-код как отсканированный

## Как использовать

1. Зарегистрируйте нового пользователя через API или веб-интерфейс
2. Сгенерируйте QR-коды и распечатайте их
3. Разместите QR-коды в разных местах
4. Отсканируйте QR-код с помощью приложения и добавьте его в свою коллекцию
5. Отслеживайте прогресс на карте и лидерборде 
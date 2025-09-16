# TestingApp - Система створення та проходження тестів

Сучасний веб-додаток для створення, публікації та проходження тестів з підтримкою Google OAuth та Telegram аутентифікації.

## 🚀 Функціональність

- **Аутентифікація**: Вхід через Google або Telegram
- **Створення тестів**: Інтуїтивний редактор з різними типами питань
- **Типи питань**:
  - Один правильний відповідь
  - Кілька правильних відповідей  
  - Відкриті питання
- **Публікація**: Унікальні 6-символьні коди для тестів
- **Проходження**: Зручний інтерфейс для проходження тестів
- **Аналітика**: Детальна статистика результатів

## 🛠 Технології

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript
- **База даних**: SQLite (можна змінити на PostgreSQL)
- **Аутентифікація**: Google OAuth, Telegram Bot API

## 📦 Встановлення

1. **Клонуйте репозиторій**:
```bash
git clone <repository-url>
cd TestingApp/backend
```

2. **Створіть віртуальне середовище**:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Встановіть залежності**:
```bash
pip install -r requirements.txt
```

4. **Налаштуйте конфігурацію**:
```bash
cp config.env .env
# Відредагуйте .env файл з вашими налаштуваннями
```

5. **Ініціалізуйте базу даних**:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Запустіть додаток**:
```bash
python src/run.py
```

## ⚙️ Конфігурація

Створіть файл `.env` з наступними параметрами:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
SQLALCHEMY_DATABASE_URI=sqlite:///quiz.db

# Google OAuth (опціонально)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Telegram Bot (опціонально)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_BOT_NAME=your-bot-name

# App Configuration
APP_BASE_URL=http://localhost:5000
```

## 🔧 Налаштування Google OAuth

1. Перейдіть до [Google Cloud Console](https://console.cloud.google.com/)
2. Створіть новий проект або оберіть існуючий
3. Увімкніть Google+ API
4. Створіть OAuth 2.0 credentials
5. Додайте `http://localhost:5000/auth/google/callback` до redirect URIs
6. Скопіюйте Client ID та Client Secret до `.env` файлу

## 🤖 Налаштування Telegram Bot

1. Створіть бота через [@BotFather](https://t.me/botfather)
2. Отримайте токен бота
3. Додайте токен та ім'я бота до `.env` файлу
4. Запустіть бота командою `/start`

## 📱 Використання

1. **Створення тесту**:
   - Увійдіть в систему
   - Натисніть "Створити тест"
   - Введіть назву тесту
   - Додайте питання різних типів
   - Опублікуйте тест

2. **Проходження тесту**:
   - Натисніть "Знайти тест"
   - Введіть 6-символьний код
   - Відповідайте на питання
   - Переглядайте результат

3. **Аналітика**:
   - Перейдіть до "Мої тести"
   - Натисніть "Результати" для перегляду статистики

## 🎨 Дизайн

Додаток використовує сучасний, адаптивний дизайн з:
- Градієнтними фонами
- Плавними анімаціями
- Інтуїтивним UX
- Підтримкою мобільних пристроїв

## 🔒 Безпека

- CSRF захист через Flask-WTF
- Валідація всіх форм
- Безпечна аутентифікація
- Захист від SQL-ін'єкцій через SQLAlchemy

## 📊 База даних

Схема бази даних включає:
- **Users**: Користувачі системи
- **Quizzes**: Тести
- **Questions**: Питання тестів
- **Choices**: Варіанти відповідей
- **Submissions**: Результати проходження
- **Answers**: Відповіді користувачів

## 🚀 Розгортання

Для продакшн середовища:

1. Змініть `SQLALCHEMY_DATABASE_URI` на PostgreSQL
2. Встановіть `SECRET_KEY` з безпечним значенням
3. Налаштуйте веб-сервер (nginx + gunicorn)
4. Налаштуйте SSL сертифікат
5. Оновіть `APP_BASE_URL` на ваш домен

## 🤝 Внесок

1. Форкніть репозиторій
2. Створіть feature branch
3. Зробіть зміни
4. Створіть Pull Request

## 📄 Ліцензія

MIT License

## 📞 Підтримка

Якщо у вас виникли питання або проблеми, створіть issue в репозиторії.

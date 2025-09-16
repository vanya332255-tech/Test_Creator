import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///quiz.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_BOT_NAME = os.getenv("TELEGRAM_BOT_NAME")
    APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:5000")
    GOOGLE_FORM_ID = os.getenv("GOOGLE_FORM_ID", "YOUR_GOOGLE_FORM_ID")
    GOOGLE_FORM_URL = os.getenv("GOOGLE_FORM_URL", "https://forms.gle/YOUR_GOOGLE_FORM_ID")


class ProductionConfig(Config):
    # Try DATABASE_URL first, then fallback to SQLite
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///quiz.db"
    APP_BASE_URL = os.getenv("APP_BASE_URL", "https://testingapp.onrender.com")
import secrets
import time
import threading
import asyncio
from flask import current_app
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


# Простое in-memory хранилище для кода подтверждения
class CodesStore:
    def __init__(self):
        self._map = {}      # phone -> telegram_user_id
        self._codes = {}    # phone -> (code, expires_ts)

    def save_mapping(self, phone: str, user_id: int):
        self._map[phone] = user_id

    def get_user_id(self, phone: str):
        return self._map.get(phone)

    def issue_code(self, phone: str, ttl: int = 300) -> str:
        """Создать одноразовый код"""
        code = f"{secrets.randbelow(1000000):06d}"
        self._codes[phone] = (code, time.time() + ttl)
        return code

    def verify(self, phone: str, code: str) -> bool:
        """Проверить код"""
        data = self._codes.get(phone)
        if not data:
            return False
        c, exp = data
        ok = (c == code and time.time() < exp)
        if ok:
            del self._codes[phone]
        return ok


codes = CodesStore()


# ==== Telegram handlers ====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка /start"""
    kb = [[KeyboardButton("Поделиться номером", request_contact=True)]]
    await update.message.reply_text(
        "Привет! Нажми кнопку ниже, чтобы поделиться телефоном и связать аккаунт.",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True)
    )


async def got_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохраняем телефон и user_id"""
    contact = update.effective_message.contact
    phone = contact.phone_number
    user_id = update.effective_user.id
    codes.save_mapping(phone, user_id)
    await update.message.reply_text("Спасибо! Телефон привязан, можешь вернуться на сайт.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """На случай произвольных сообщений"""
    await update.message.reply_text("Напиши /start и поделись номером, чтобы привязать телефон.")


async def send_code(phone: str, code: str) -> bool:
    """Отправить код в Telegram"""
    app = current_app.telegram_app
    user_id = codes.get_user_id(phone)
    if not user_id:
        return False
    await app.bot.send_message(chat_id=user_id, text=f"Ваш код подтверждения: {code}")
    return True


# ==== Инициализация бота ====

def init_telegram(app):
    token = app.config.get("TELEGRAM_BOT_TOKEN")
    if not token:
        return

    tg_app = Application.builder().token(token).build()
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(MessageHandler(filters.CONTACT, got_contact))
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.telegram_app = tg_app

    # запуск в отдельном потоке, чтобы не блокировал Flask
    threading.Thread(target=lambda: asyncio.run(tg_app.run_polling()), daemon=True).start()

import secrets
import time
import threading
import asyncio
from flask import current_app
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


# --- Простое in-memory хранилище кодов ---
class CodesStore:
    def __init__(self):
        self._map = {}  # phone -> telegram_user_id
        self._codes = {}  # phone -> (code, expires_ts)

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


# --- Handlers для бота ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[KeyboardButton("Поделиться номером", request_contact=True)]]
    await update.message.reply_text(
        "Привет! Нажми кнопку ниже, чтобы поделиться телефоном и связать аккаунт.",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True)
    )


async def got_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.effective_message.contact
    phone = contact.phone_number
    user_id = update.effective_user.id
    codes.save_mapping(phone, user_id)
    await update.message.reply_text("Спасибо! Телефон привязан, теперь можно вернуться на сайт.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши /start и поделись номером, чтобы привязать телефон.")


# --- Отправка кода ---
async def send_code(phone: str, code: str) -> bool:
    app = current_app
    tg_app = getattr(app, "telegram_app", None)
    if not tg_app:
        app.logger.error("❌ Telegram bot не инициализирован")
        return False

    user_id = codes.get_user_id(phone)
    if not user_id:
        return False

    await tg_app.bot.send_message(chat_id=user_id, text=f"Ваш код подтверждения: {code}")
    return True


# --- Инициализация бота ---
def init_telegram(app):
    token = app.config.get("TELEGRAM_BOT_TOKEN")
    if not token:
        app.logger.warning("⚠️ TELEGRAM_BOT_TOKEN не задан — бот не запущен")
        return

    tg_app = Application.builder().token(token).build()

    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(MessageHandler(filters.CONTACT, got_contact))
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # сохраняем бота в Flask
    app.telegram_app = tg_app

    # запускаем polling в отдельном потоке
    def _run():
        asyncio.run(tg_app.run_polling())

    threading.Thread(target=_run, daemon=True).start()
    app.logger.info("✅ Telegram bot запущен")

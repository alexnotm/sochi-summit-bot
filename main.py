import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- утилиты
def _short(s: str, n: int = 8) -> str:
    return s[:n] + "…" if s and len(s) > n else (s or "")

def get_env(*keys, default=None):
    for k in keys:
        v = os.getenv(k)
        if v:
            print(f"[ENV] Найдено {k} = '{_short(v)}'")
            return v
    print(f"[ENV] Не найдено ни одно из ключей: {', '.join(keys)}")
    return default

# --- читаем токен/ID из разных вариантов переменных
BOT_TOKEN = get_env("BOT_TOKEN", "TELEGRAM_BOT_TOKEN", "TOKEN")
ADMIN_ID_RAW = get_env("ADMIN_ID", "OWNER_ID", "ADMIN", default="")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN отсутствует. Проверь Variables в СЕРВИСЕ (не на уровне проекта).")
    print("   Должно быть ровно:  BOT_TOKEN = <твой токен от BotFather>")
    sys.exit(1)

try:
    ADMIN_ID = int(ADMIN_ID_RAW)
except Exception:
    print("❌ ADMIN_ID отсутствует или не число. Укажи переменную окружения:")
    print("   ADMIN_ID = 294491997   (без кавычек)")
    sys.exit(1)

# --- обработчик: пересылаем всё админу
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message:
            return
        user = update.message.from_user
        name = user.username or user.full_name or "Без_имени"
        print(f"[LOG] Входящее сообщение от: {name} (id={user.id})")

        # пересылаем сообщение админу
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

        # подпись кто написал
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Сообщение от @{name} (id: {user.id})"
        )

        # ответ пользователю
        await update.message.reply_text(
            "✅ Спасибо! Ваше сообщение отправлено организаторам Sochi Summit."
        )
    except Exception as e:
        print(f"⚠️ Ошибка при пересылке: {e}")

# --- запуск бота ---
if __name__ == "__main__":
    print("🚀 Запуск бота…")
    print(f"[CHECK] BOT_TOKEN начинается с: '{_short(BOT_TOKEN)}'")
    print(f"[CHECK] ADMIN_ID = {ADMIN_ID}")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, forward_message))
    print("🤖 Бот запущен. Жду сообщения…")
    app.run_polling()

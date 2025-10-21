import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# === Получаем данные из переменных окружения ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Проверки наличия переменных
if not BOT_TOKEN:
    raise ValueError("❌ Переменная BOT_TOKEN не найдена! Добавь её в Railway Variables.")
if not ADMIN_ID:
    raise ValueError("❌ Переменная ADMIN_ID не найдена! Добавь её в Railway Variables.")

ADMIN_ID = int(ADMIN_ID)

# === Обработчик входящих сообщений ===
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.message.from_user
        name = user.username or user.full_name or "Без имени"
        text = f"📩 Новое сообщение от @{name}:"

        print(f"[LOG] Получено сообщение от {name}")  # для Railway Logs

        # Пересылаем сообщение админу
        await context.bot.send_message(chat_id=ADMIN_ID, text=text)
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

        # Ответ пользователю
        await update.message.reply_text(
            "✅ Спасибо! Ваше сообщение отправлено организаторам Sochi Summit."
        )

    except Exception as e:
        print(f"⚠️ Ошибка при пересылке: {e}")

# === Запуск приложения ===
if __name__ == "__main__":
    print("🚀 Бот запускается...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, forward_message))
    print("🤖 Бот успешно запущен и ждёт сообщений.")
    app.run_polling()

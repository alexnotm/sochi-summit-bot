import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not ADMIN_ID:
    print("⚠️ Ошибка: переменная ADMIN_ID не найдена в окружении Railway!")
else:
    ADMIN_ID = int(ADMIN_ID)

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    name = user.username or user.full_name
    text = f"📩 Новое сообщение от @{name}:"
    print(f"Получено сообщение от {name}")  # лог в Railway

    if ADMIN_ID:
        await context.bot.send_message(chat_id=ADMIN_ID, text=text)
        await context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        await update.message.reply_text("✅ Ваше сообщение отправлено организаторам саммита.")
    else:
        await update.message.reply_text("⚠️ Ошибка: администратор не настроен. Свяжитесь с поддержкой.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, forward_message))

print("🚀 Бот запущен и ждёт сообщений...")
app.run_polling()

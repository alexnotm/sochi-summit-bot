import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# === Настройки через окружение ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = f"📩 Новое сообщение от @{user.username or user.full_name}:"
    await context.bot.forward_message(chat_id=f"@{ADMIN_USERNAME}", from_chat_id=update.message.chat_id, message_id=update.message.message_id)
    await context.bot.send_message(chat_id=f"@{ADMIN_USERNAME}", text=text)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, forward_message))

print("Бот запущен 🚀")
app.run_polling()

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# === Настройки ===
BOT_TOKEN = "8340460681:AAGqKHUS1vcAk0Gc4JN8X8m2YUFI-qQfZyE"
ADMIN_USERNAME = "Geoplatform"  # твой Telegram @username

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = f"📩 Новое сообщение от @{user.username or user.full_name}:"
    
    # Пересылаем само сообщение
    await context.bot.forward_message(chat_id=f"@{ADMIN_USERNAME}", from_chat_id=update.message.chat_id, message_id=update.message.message_id)
    # Отправляем уведомление с именем
    await context.bot.send_message(chat_id=f"@{ADMIN_USERNAME}", text=text)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, forward_message))

print("Бот запущен 🚀")
app.run_polling()

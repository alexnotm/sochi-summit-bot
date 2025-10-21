import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# === Настройки ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # теперь используем числовой ID

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    name = user.username or user.full_name
    text = f"📩 Новое сообщение от @{name}:"

    # Отправляем уведомление и пересылаем сообщение
    await context.bot.send_message(chat_id=ADMIN_ID, text=text)
    await context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)

    # Подтверждение пользователю
    await update.message.reply_text("✅ Спасибо! Ваше сообщение отправлено организаторам саммита.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, forward_message))

print("Бот запущен 🚀")
app.run_polling()

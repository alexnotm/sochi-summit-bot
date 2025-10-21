from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8340460681:AAGqKHUS1vcAk0Gc4JN8X8m2YUFI-qQfZyE"
ADMIN_ID = 294491997

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user = update.message.from_user
    name = user.username or user.full_name or "Без_имени"
    text = update.message.text or "(медиа)"

    print(f"[LOG] Получено сообщение от @{name}: {text}")

    try:
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Сообщение от @{name} (id: {user.id})"
        )
        await update.message.reply_text("✅ Спасибо! Ваше сообщение отправлено организаторам Sochi Summit.")
    except Exception as e:
        print(f"⚠️ Ошибка при пересылке: {e}")

if __name__ == "__main__":
    print("🚀 Бот запускается...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, forward_message))
    print("🤖 Бот запущен и ждёт сообщений...")
    app.run_polling()

# --- ВРЕМЕННАЯ ВЕРСИЯ ДЛЯ ЗАПУСКА БЕЗ ОКРУЖЕНИЯ ---
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ВСТАВЛЯЕМ ЗНАЧЕНИЯ НАПРЯМУЮ
BOT_TOKEN = "8340460681:AAGqKHUS1vcAk0Gc4JN8X8m2YUFI-qQfZyE"
ADMIN_ID  = 294491997  # твой ID

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user = update.message.from_user
    name = user.username or user.full_name or "Без_имени"
    # 1) пересылаем оригинал тебе
    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )
    # 2) подпись кто писал
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 Сообщение от @{name} (id: {user.id})"
    )
    # 3) автоответ пользователю
    await update.message.reply_text("✅ Ваше сообщение отправлено организаторам Sochi Summit.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, forward_message))
app.run_polling()

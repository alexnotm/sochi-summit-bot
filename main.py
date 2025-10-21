from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# === НАСТРОЙКИ ===
BOT_TOKEN = "8340460681:AAGqKHUS1vcAk0Gc4JN8X8m2YUFI-qQfZyE"  # токен бота
ADMIN_ID = 294491997  # твой Telegram ID (@Geoplatform)

# === ФУНКЦИЯ: пересылка сообщений ===
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return  # пропускаем системные события

    user = update.message.from_user
    name = user.username or user.full_name or "Без_имени"
    text = update.message.text or "(медиа)"

    print(f"[LOG] Получено сообщение от @{name}: {text}")

    try:
        # 1️⃣ Пересылаем сообщение админу
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

        # 2️⃣ Подпись: кто написал
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Сообщение от @{name} (id: {user.id})"
        )

        #

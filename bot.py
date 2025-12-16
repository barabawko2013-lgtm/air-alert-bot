from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Отримуємо токен бота з Environment Variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN не задано в змінних оточення!")
    exit(1)

# Створюємо додаток бота
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Бот запущений ✅")

# Додаємо команду /start
app.add_handler(CommandHandler("start", start))

# Запускаємо бота
if __name__ == "__main__":
    print("Бот запускається...")
    app.run_polling()

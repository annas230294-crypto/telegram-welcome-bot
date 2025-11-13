import os
from telegram.ext import Application, CommandHandler

# Получаем токен
def get_bot_token():
    try:
        with open('/etc/secrets/BOT_TOKEN_NEW', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return os.getenv('BOT_TOKEN')

BOT_TOKEN = get_bot_token()

# Создаем бота
bot_app = Application.builder().token(BOT_TOKEN).build()

async def start(update, context):
    user_name = update.message.from_user.first_name
    welcome_text = f"""
<b>Привет, {user_name}!</b>

Добро пожаловать в мир безграничного творчества с нейросетями!

Мой канал: @code_and_beauty
    """
    await update.message.reply_text(welcome_text, parse_mode='HTML')

# Добавляем обработчик
bot_app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN не найден!")
    
    print("✅ Токен загружен успешно")
    print("🚀 Запускаем бота...")
    
    # Просто запускаем бота
    bot_app.run_polling(drop_pending_updates=True)
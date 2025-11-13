import os
from flask import Flask
import threading
from telegram.ext import Application, CommandHandler
import asyncio

app = Flask(__name__)

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

def run_bot():
    print("Starting Telegram bot...")
    # Запускаем поллинг в event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot_app.run_polling(drop_pending_updates=True)

@app.route('/')
def health_check():
    return "✅ Bot is running and healthy!", 200

@app.route('/health')
def health():
    """Простой endpoint для мониторинга"""
    return "OK", 200

if __name__ == "__main__":
    # Проверяем токен
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN не найден!")
    
    print("✅ Токен загружен успешно")
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # Запускаем Flask сервер на правильном порту
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
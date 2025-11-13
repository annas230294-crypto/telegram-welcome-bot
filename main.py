import os
from flask import Flask
import threading
from telegram.ext import Application, CommandHandler

app = Flask(__name__)
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Создаем бота
bot_app = Application.builder().token(BOT_TOKEN).build()

async def start(update, context):
    user_name = update.message.from_user.first_name
    welcome_text = f"""
🎨 <b>Привет, {user_name}!</b>
Ты попал(а) в мир безграничного творчества с нейросетями! 
🤖 Мой канал: @code_and_beauty
    """
    await update.message.reply_text(welcome_text, parse_mode='HTML')

# Добавляем обработчик
bot_app.add_handler(CommandHandler("start", start))

def run_bot():
    print("🤖 Starting Telegram bot...")
    bot_app.run_polling(drop_pending_updates=True)

@app.route('/')
def health_check():
    return "✅ Bot is running and healthy!", 200

@app.route('/health')
def health():
    """Простой endpoint для мониторинга"""
    return "OK", 200

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Запускаем Flask сервер на правильном порту
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
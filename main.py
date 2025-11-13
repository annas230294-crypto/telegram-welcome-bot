import os
import time
import sys
import threading
import requests
from flask import Flask, jsonify
from telegram.ext import Application, CommandHandler
from telegram.error import Conflict, TelegramError

app = Flask(__name__)

# Получаем токен
def get_bot_token():
    try:
        with open('/etc/secrets/BOT_TOKEN_NEW', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return os.getenv('BOT_TOKEN')

BOT_TOKEN = get_bot_TOKEN()
RENDER_URL = "https://telegram-bot-new-9ymy.onrender.com"  # Ваш URL

# Создаем бота
bot_app = Application.builder().token(BOT_TOKEN).build()

async def start(update, context):
    user_name = update.message.from_user.first_name
    welcome_text = f"""🎨 <b>Привет, {user_name}!</b>

Ты попал(а) в мир безграничного творчества с нейросетями! 

🤖 <b>Мой канал:</b> @code_and_beauty

✨ <b>Что тебя ждет внутри:</b>
🔥 Готовые, бесплатные, кастомные промты для самых популярных нейросетей
🚀 Бустерные промты для твоих шедевров в один клик
💡 Трендовые стили: от аниме до гиперреализма
🎯 Рабочие связки для сложных сцен и персонажей
📈 Обзоры новых нейросетей и их возможностей
👥 Сообщество единомышленников

💫 <b>Подпишись и получи доступ к:</b>
• Библиотеке из 500+ готовых промтов
• Гайдам по созданию уникальных изображений
• Ежедневным порциям вдохновения
• Эксклюзивным материалам

⚡ <b>Преврати простой текст в цифровое искусство вместе со мной!</b>

✅ <b>Подпишись на канал и открой мир AI-творчества!</b>"""

    await update.message.reply_text(welcome_text, parse_mode='HTML')

# Добавляем обработчик
bot_app.add_handler(CommandHandler("start", start))

# 🔧 ФУНКЦИЯ АВТО-ПИНГА (чтобы бот не засыпал)
def auto_ping():
    """Пинг самого себя каждые 10 минут"""
    while True:
        try:
            # Пингуем основной URL
            response = requests.get(RENDER_URL, timeout=10)
            print(f"✅ Авто-пинг: {response.status_code} - {time.strftime('%H:%M:%S')}")
            
            # Пингуем health endpoint
            health_response = requests.get(f"{RENDER_URL}/bot-health", timeout=10)
            print(f"✅ Health check: {health_response.status_code}")
            
        except Exception as e:
            print(f"❌ Ошибка авто-пинга: {e}")
        
        # Ждем 10 минут (600 секунд)
        time.sleep(600)

# 🔧 ENDPOINT ДЛЯ ПРАВИЛЬНОГО МОНИТОРИНГА
@app.route('/bot-health')
def bot_health():
    try:
        # Проверяем, что бот подключен к Telegram API
        bot_info = bot_app.bot.get_me()
        return jsonify({
            "status": "healthy",
            "bot_name": bot_info.first_name,
            "bot_username": bot_info.username,
            "bot_id": bot_info.id,
            "timestamp": time.time(),
            "message": "✅ Бот полностью функционирует"
        }), 200
    except TelegramError as e:
        return jsonify({
            "status": "error", 
            "error": str(e),
            "timestamp": time.time(),
            "message": "❌ Ошибка подключения к Telegram"
        }), 500

@app.route('/')
def home():
    return """
    <h1>🤖 Telegram Bot Active</h1>
    <p>Бот работает и не спит!</p>
    <p><a href="/bot-health">Проверить статус бота</a></p>
    <p>Последнее обновление: {}</p>
    """.format(time.strftime('%Y-%m-%d %H:%M:%S'))

def run_bot():
    print("Starting Telegram bot...")
    try:
        bot_app.run_polling(
            drop_pending_updates=True,
            allowed_updates=['message']
        )
    except Conflict:
        print("❌ Conflict detected. Exiting...")
        sys.exit(1)

if __name__ == "__main__":
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN не найден!")
    
    print("✅ Токен загружен успешно")
    
    # Запускаем авто-пинг в отдельном потоке
    ping_thread = threading.Thread(target=auto_ping, daemon=True)
    ping_thread.start()
    print("🚀 Авто-пинг запущен (каждые 10 минут)")
    
    # Запускаем бот в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print("🤖 Бот запущен")
    
    # Запускаем Flask сервер
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Flask сервер запускается на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
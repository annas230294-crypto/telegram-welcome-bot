import os
import time
import threading
from flask import Flask, jsonify
from telegram.ext import Application, CommandHandler
from telegram.error import Conflict
import urllib.request

app = Flask(__name__)

# Получаем токен
def get_bot_token():
    try:
        with open('/etc/secrets/BOT_TOKEN_NEW', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return os.getenv('BOT_TOKEN')

BOT_TOKEN = get_bot_token()
RENDER_URL = "https://telegram-bot-new-9ymy.onrender.com"

# Создаем бота
if BOT_TOKEN:
    bot_app = Application.builder().token(BOT_TOKEN).build()
else:
    bot_app = None
    print("❌ Токен не найден!")

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

# Функция авто-пинга
def auto_ping():
    while True:
        try:
            with urllib.request.urlopen(RENDER_URL, timeout=10) as response:
                print(f"✅ Авто-пинг: {response.getcode()} - {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"❌ Ошибка авто-пинга: {e}")
        time.sleep(300)  # 5 минут

# Функция запуска бота
def run_bot():
    if bot_app:
        try:
            bot_app.add_handler(CommandHandler("start", start))
            print("🤖 Бот запускается...")
            bot_app.run_polling(drop_pending_updates=True)
        except Conflict:
            print("❌ Конфликт! Ждем 30 секунд...")
            time.sleep(30)
            run_bot()  # Перезапускаем
    else:
        print("❌ Бот не может запуститься - нет токена")

@app.route('/bot-health')
def bot_health():
    if bot_app:
        try:
            bot_info = bot_app.bot.get_me()
            return jsonify({
                "status": "healthy",
                "bot_name": bot_info.first_name,
                "message": "✅ Бот работает"
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "Бот не инициализирован"}), 500

@app.route('/')
def home():
    return "🤖 Бот активен" if bot_app else "❌ Бот не запущен"

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Запуск системы...")
    
    if BOT_TOKEN:
        print("✅ Токен загружен")
        
        # Запускаем авто-пинг
        ping_thread = threading.Thread(target=auto_ping, daemon=True)
        ping_thread.start()
        print("🔔 Авто-пинг запущен")
        
        # Запускаем бота
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        print("🤖 Поток бота запущен")
    else:
        print("❌ ТОКЕН НЕ НАЙДЕН!")
    
    # Запускаем Flask
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Flask запускается на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
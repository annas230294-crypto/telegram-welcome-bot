import os
import time
import asyncio
from flask import Flask, jsonify
from telegram.ext import Application, CommandHandler
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

print(f"🔑 Токен: {'***' + BOT_TOKEN[-4:] if BOT_TOKEN else 'НЕ НАЙДЕН'}")

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
    print(f"✅ Отправлено приветствие пользователю: {user_name}")

# Добавляем обработчик
bot_app.add_handler(CommandHandler("start", start))

# Функция авто-пинга
def auto_ping():
    while True:
        try:
            with urllib.request.urlopen(RENDER_URL, timeout=10) as response:
                print(f"✅ Авто-пинг: {response.getcode()} - {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"❌ Ошибка авто-пинга: {e}")
        time.sleep(300)  # 5 минут

# Функция запуска бота в отдельном потоке с event loop
def run_bot():
    print("🤖 Создаем event loop для бота...")
    
    # Создаем новый event loop для этого потока
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        print("🤖 Запускаем поллинг бота...")
        bot_app.run_polling(
            drop_pending_updates=True,
            allowed_updates=['message']
        )
    except Exception as e:
        print(f"❌ Ошибка бота: {e}")
        print("🔄 Перезапуск через 30 секунд...")
        time.sleep(30)
        run_bot()

@app.route('/bot-health')
def bot_health():
    try:
        # Используем asyncio для асинхронного вызова
        async def get_bot_info():
            return await bot_app.bot.get_me()
        
        # Запускаем в event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bot_info = loop.run_until_complete(get_bot_info())
        loop.close()
        
        return jsonify({
            "status": "healthy",
            "bot_name": bot_info.first_name,
            "bot_username": bot_info.username,
            "message": "✅ Бот работает и принимает сообщения"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/')
def home():
    return "🤖 Бот активен - используйте /start в Telegram"

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 ЗАПУСК СИСТЕМЫ")
    
    if not BOT_TOKEN:
        print("❌ КРИТИЧЕСКАЯ ОШИБКА: Токен не найден!")
        exit(1)
    
    print("✅ Токен загружен")
    
    # Запускаем авто-пинг в отдельном потоке
    import threading
    ping_thread = threading.Thread(target=auto_ping, daemon=True)
    ping_thread.start()
    print("🔔 Авто-пинг запущен")
    
    # Запускаем бота в ОСНОВНОМ потоке (без threading)
    print("🤖 ЗАПУСКАЕМ БОТА В ОСНОВНОМ ПОТОКЕ...")
    run_bot()
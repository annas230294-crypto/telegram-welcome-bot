import os
import time
import threading
from telegram.ext import Application, CommandHandler

print("=" * 50)
print("🚀 ЗАПУСК БОТА - ОБХОД FLASK")

# Получаем токен
def get_bot_token():
    try:
        with open('/etc/secrets/BOT_TOKEN_NEW', 'r') as f:
            token = f.read().strip()
            print(f"✅ Токен: ***{token[-4:]}")
            return token
    except Exception as e:
        print(f"❌ Ошибка токена: {e}")
        return None

BOT_TOKEN = get_bot_token()

if not BOT_TOKEN:
    print("❌ ТОКЕН НЕ НАЙДЕН!")
    exit(1)

# Создаем бота
bot_app = Application.builder().token(BOT_TOKEN).build()

async def start(update, context):
    user_name = update.message.from_user.first_name
    welcome_text = f"""🎨 <b>Привет, {user_name}!</b>

Ты попал(а) в мир безграничного творчества с нейросетями! 

🤖 <b>Мой канал:</b> @code_and_beauty

✨ <b>Что тебя ждет внутри:</b>
🔥 Готовые, бесплатные, кастомные промты
🚀 Бустерные промты для шедевров
💡 Трендовые стили
🎯 Рабочие связки
📈 Обзоры нейросетей
👥 Сообщество"""

    await update.message.reply_text(welcome_text, parse_mode='HTML')
    print(f"✅ Отправлено: {user_name}")

bot_app.add_handler(CommandHandler("start", start))

# 🔧 ЗАПУСКАЕМ БОТА В ОТДЕЛЬНОМ ПОТОКЕ СРАЗУ
def run_bot():
    print("🤖 ЗАПУСКАЕМ ТЕЛЕГРАМ БОТА...")
    bot_app.run_polling(drop_pending_updates=True)

# Запускаем бота сразу при импорте
bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()

print("✅ Бот запущен в фоне!")

# 🔧 ОБХОД: Создаем минимальный Flask чтобы Render был доволен
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Бот работает"

@app.route('/health')
def health():
    return "OK", 200

# 🔧 ОБХОД: Запускаем Flask только формально
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Flask запускается на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
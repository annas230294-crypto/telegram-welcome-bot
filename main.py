import os
from telegram.ext import Application, CommandHandler

print("=" * 50)
print("🚀 ЗАПУСК БОТА")

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

print("✅ Бот запускается...")
bot_app.run_polling(drop_pending_updates=True)
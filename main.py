import os
import time
from flask import Flask
from telegram.ext import Application, CommandHandler
import threading

app = Flask(__name__)

def get_bot_token():
    try:
        with open('/etc/secrets/BOT_TOKEN_NEW', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return os.getenv('BOT_TOKEN')

BOT_TOKEN = get_bot_token()

if BOT_TOKEN:
    bot_app = Application.builder().token(BOT_TOKEN).build()

    async def start(update, context):
        user_name = update.message.from_user.first_name
        welcome_text = f"""🎨 <b>Привет, {user_name}!</b>"""
        # ... ваш текст ...
        await update.message.reply_text(welcome_text, parse_mode='HTML')
        print(f"✅ Отправлено: {user_name}")

    bot_app.add_handler(CommandHandler("start", start))

    def run_bot():
        print("🤖 Бот запускается...")
        bot_app.run_polling(drop_pending_updates=True)

    # Запускаем бота при импорте
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

@app.route('/')
def home():
    return "Бот работает"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import Conflict

BOT_TOKEN = os.getenv('BOT_TOKEN')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if isinstance(context.error, Conflict):
        print("Обнаружен конфликт - вероятно, бот запущен в двух местах")
    else:
        print(f'Ошибка: {context.error}')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    
    # ОБНОВЛЕННОЕ ПРИВЕТСТВЕННОЕ СООБЩЕНИЕ
    welcome_text = f"""
🎨 <b>Привет, {user_name}!</b>

Ты попал(а) в мир безграничного творчества с нейросетями! 

🤖 Мой канал: @code_and_beauty

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

✅ <b>Подпишись на канал и открой мир AI-творчества!</b>
    """
    await update.message.reply_text(welcome_text, parse_mode='HTML')

# Простой HTTP сервер для проверки работоспособности
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is running and healthy!")
    
    def log_message(self, format, *args):
        pass  # Отключаем логи

def run_web():
    server = HTTPServer(('0.0.0.0', 5000), Handler)
    print("Web server started on port 5000")
    server.serve_forever()

if __name__ == "__main__":
    # Запускаем веб-сервер в отдельном потоке
    web_thread = threading.Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()

    # Запускаем бота
    bot = Application.builder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_error_handler(error_handler)

    print("Бот запущен!")
    bot.run_polling()
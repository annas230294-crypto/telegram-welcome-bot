import os
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
    await update.message.reply_text("Бот работает! 💍")

# Простой HTTP сервер для порта
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    
    def log_message(self, format, *args):
        pass  # Отключаем логи

def run_web():
    server = HTTPServer(('0.0.0.0', 5000), Handler)
    print("Web server started on port 5000")
    server.serve_forever()

if __name__ == "__main__":
    import threading

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
import os
import asyncio
from threading import Thread
import socket
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8311994813:AAENv4Ag2bUxsiP4_kdzJAXDsznD9rwTA3c"

# ==== ЗАНИМАЕМ ПОРТ ДЛЯ RENDER ====
def bind_port():
    port = int(os.environ.get('PORT', 8080))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', port))
    sock.listen(1)
    print(f"📄 Port {port} is bound for Render")
    while True:
        try:
            client, addr = sock.accept()
            client.send(b'HTTP/1.1 200 OK\r\n\r\nBot is running')
            client.close()
        except:
            continue

port_thread = Thread(target=bind_port, daemon=True)
port_thread.start()
# ==== КОНЕЦ БЛОКА ДЛЯ ПОРТА ====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name or "Аноним"
    
    keyboard = [
        [InlineKeyboardButton("✔ ПОДПИСАТЬСЯ НА КАНАЛ", url="https://t.me/code_and_beauty")],
        [InlineKeyboardButton("✔ Я ПОДПИСАН(a)!", callback_data="subscribed")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = f"""Привет, {user_name}! 👋

Ты попал(a) в мир безграничного творчества с нейросетями! 🎨✨

Мой канал: @code_and_beauty

Что тебя ждет внутри:
• 🎯 Готовые, бесплатные, кастомные промты
• 🚀 Бустерные промты для твоих шедевров
• 🌟 Трендовые стили: от аниме до гиперреализма
• 💫 Рабочие связки для сложных сцен
• 🔥 Обзоры новых нейросетей
• 👥 Сообщество единомышленников

Подпишись и получи доступ к:
• 📚 Библиотеке из 500+ готовых промтов
• 📖 Гайдам по созданию изображений
• 💡 Ежедневным порциям вдохновения
• 🎁 Эксклюзивным материалам

Преврати простой текст в цифровое искусство! 🟧✨

Подпишись на канал и открой мир AI-творчества! 🎭"""
    
    await update.message.reply_text(message_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_name = query.from_user.first_name or "Аноним"
    await query.answer()
    
    if query.data == "subscribed":
        await query.message.reply_text(f"Отлично, {user_name}! 🎉\n\nТеперь ты получил(а) доступ ко всем материалам канала! 📚✨")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("BOT ЗАПУЩЕН! Ожидаем сообщения...")
    app.run_polling()

if __name__ == "__main__":
    main()
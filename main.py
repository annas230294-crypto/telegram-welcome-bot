from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler

TOKEN = "8311994813:AAENv4Ag2bUxsiP4_kdzJAXDsznD9rwTA3c"

async def start(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.first_name or "друг"
    
    # Создаем кнопки
    keyboard = [
        [InlineKeyboardButton("📱 Подписаться на канал", url="https://t.me/code_and_beauty")],
        [InlineKeyboardButton("✅ Я подписан(а)", callback_data="subscribed")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Текст сообщения
    message_text = f"""🎨 Привет, {user_name}!

Ты попал(а) в мир безграничного творчества с нейросетями! 

🤖 Мой канал: @code_and_beauty

✨ Что тебя ждет внутри:
🔥 Готовые, бесплатные, кастомные промты
🚀 Бустерные промты для твоих шедевров
💡 Трендовые стили: от аниме до гиперреализма
🎯 Рабочие связки для сложных сцен
📈 Обзоры новых нейросетей
👥 Сообщество единомышленников

💫 Подпишись и получи доступ к:
• Библиотеке из 500+ готовых промтов
• Гайдам по созданию изображений
• Ежедневным порциям вдохновения
• Эксклюзивным материалам

⚡ Преврати простой текст в цифровое искусство!

✅ Подпишись на канал и открой мир AI-творчества!"""
    
    await update.message.reply_text(message_text, reply_markup=reply_markup)

# Обработчик кнопки
async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_name = query.from_user.first_name or "друг"
    
    await query.answer()
    
    if query.data == "subscribed":
        await query.message.reply_text(f"🎉 Отлично, {user_name}! Вот твои промты:\n\nhttps://t.me/code_and_beauty\n\nЕсли есть проблемы, напиши @username")

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🟢 БОТ ЗАПУЩЕН! Ожидаем сообщения...")
    app.run_polling()

if __name__ == "__main__":
    main()
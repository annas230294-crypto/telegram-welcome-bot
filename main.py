from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler

async def start(update: Update, context: CallbackContext) -> None:
    # Получаем имя пользователя
    user = update.message.from_user
    user_name = user.first_name or "друг"
    
    # Создаем инлайн-кнопки
    keyboard = [
        [InlineKeyboardButton("📱 Подписаться на канал", url="https://t.me/code_and_beauty")],
        [InlineKeyboardButton("✅ Я подписан(а)", callback_data="subscribed")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Текст сообщения с подставленным именем пользователя
    message_text = f"""🎨 *Привет, {user_name}!*

Ты попал(а) в мир безграничного творчества с нейросетями! 

🤖 *Мой канал:* @code_and_beauty

---

✨ *Что тебя ждет внутри:*
🔥 Готовые, бесплатные, кастомные промты для самых популярных нейросетей
🚀 Бустерные промты для твоих шедевров в один клик
💡 Трендовые стили: от аниме до гиперреализма
🎯 Рабочие связки для сложных сцен и персонажей
📈 Обзоры новых нейросетей и их возможностей
👥 Сообщество единомышленников

---

💫 *Подпишись и получи доступ к:*
• Библиотеке из 500+ готовых промтов
• Гайдам по созданию уникальных изображений
• Ежедневным порциям вдохновения
• Эксклюзивным материалам

---

⚡ *Преврати простой текст в цифровое искусство вместе со мной!*

✅ *Подпишись на канал и открой мир AI-творчества!*"""
    
    # Отправляем сообщение с кнопками
    await update.message.reply_text(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Обработчик для кнопки "Я подписан(а)"
async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = query.from_user
    user_name = user.first_name or "друг"
    
    await query.answer()
    
    if query.data == "subscribed":
        # Проверка подписки (нужно будет добавить реальную проверку)
        await query.message.reply_text(
            f"🎉 *Отлично, {user_name}! Вот твои промты:*\n\n"
            "🔗 [Ссылка на библиотеку промтов](https://t.me/code_and_beauty)\n\n"
            "Если возникли проблемы с доступом, напиши @username",
            parse_mode="Markdown"
        )

def main():
    # Создаем приложение
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
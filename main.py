import os
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = os.getenv('BOT_TOKEN')

def start(update, context):
    update.message.reply_text("Бот работает! ✅")

updater = Updater(BOT_TOKEN)
updater.dispatcher.add_handler(CommandHandler("start", start))

print("Бот запущен!")
updater.start_polling()
updater.idle()

import os
from flask import Flask
from telegram.ext import Application, CommandHandler

BOT_TOKEN = os.getenv('BOT_TOKEN')
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running! ✅"

def start(update, context):
    update.message.reply_text("Бот работает! ✅")

if __name__ == "__main__":
    bot = Application.builder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.run_polling()
    app.run(host='0.0.0.0', port=5000)
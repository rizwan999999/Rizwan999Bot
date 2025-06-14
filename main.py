import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from keep_alive import keep_alive
import openai

# 🔐 Token और API Key
TELEGRAM_BOT_TOKEN = 8190615401:AAE9ejnAnWpi-0gPB1E6yUsKxrYvU9w1R6A
OPENAI_API_KEY = "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"

# OpenAI सेटअप
openai.api_key = OPENAI_API_KEY

# Start Command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot चालू है! /ask के साथ सवाल पूछें।")

# Ask Command
def ask(update: Update, context: CallbackContext):
    question = ' '.join(context.args)
    if not question:
        update.message.reply_text("❌ कृपया सवाल लिखें। उदाहरण: /ask भारत का प्रधानमंत्री कौन है?")
        return
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        reply = response['choices'][0]['message']['content']
        update.message.reply_text(reply)
    except Exception as e:
        update.message.reply_text("⚠️ Error: " + str(e))

# Bot को चालू रखो
keep_alive()
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("ask", ask))
updater.start_polling()
print("✅ Bot is running...")

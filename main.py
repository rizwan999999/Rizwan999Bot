
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai
import os
import asyncio

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Aviator signal function
async def send_aviator_signal(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    await context.bot.send_message(chat_id=chat_id, text="🎯 Lagao ya Na Lagao Signal: LAGAO ✅")

# /ask command handler
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("❗Usage: /ask your question")
        return

    question = " ".join(context.args)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content.strip()
        await update.message.reply_text(answer)
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        await update.message.reply_text("⚠️ Error from OpenAI API.")

# Start bot and job queue
async def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("ask", ask))

    # Aviator auto job every 2 minutes (for a fixed group/channel)
    # Replace YOUR_CHAT_ID with actual chat/group ID (as integer)
    # app.job_queue.run_repeating(send_aviator_signal, interval=120, first=10, chat_id=YOUR_CHAT_ID)

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == '__main__':
    asyncio.run(main())

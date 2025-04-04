import os
import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from flask import Flask

# Set up OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Flask app (if needed for webhook)
app = Flask(__name__)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! چطور می‌تونم کمکت کنم؟")

# Handle text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.chat_completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        reply = "مشکلی پیش اومده. لطفاً بعداً دوباره امتحان کن."

    await update.message.reply_text(reply)

# Start the bot
def run_bot():
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    application.run_polling()

# Flask route (optional, for webhook confirmation)
@app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    run_bot()
    # Optional: If you want Flask to serve something
    # app.run(debug=True)

import openai
import os
from flask import Flask, request
import telegram
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Telegram Bot with your Bot Token
bot = telegram.Bot(token=os.getenv("BOT_TOKEN"))

# Define the function to handle user messages
def handle_message(update: Update, context):
    user_message = update.message.text  # Get the text message from the user

    try:
        # OpenAI API call using the new chat completion method
        response = openai.chat_completions.create(
            model="gpt-3.5-turbo",  # You can also use "gpt-4" if you have access
            messages=[{"role": "user", "content": user_message}]
        )
        
        reply = response['choices'][0]['message']['content']
        update.message.reply_text(reply)  # Send the reply back to the user

    except Exception as e:
        print(f"Error: {e}")
        update.message.reply_text("مشکلی پیش اومده. لطفاً بعداً دوباره امتحان کن.")

# Setup the Telegram handler and updater
def start(update: Update, context):
    update.message.reply_text("سلام! چطور میتونم به شما کمک کنم؟")

def main():
    updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher

    # Define the handlers
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(Filters.text & ~Filters.command, handle_message)

    # Add handlers to the dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)

    # Start the bot
    updater.start_polling()

# Run the Flask app
if __name__ == '__main__':
    main()
    app.run(debug=True)

import os
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram import Update
import requests
from flask import Flask, request

TOKEN = os.environ["BOT_TOKEN"]
HF_TOKEN = os.environ["HF_TOKEN"]

app = Flask(__name__)

def query(payload):
    response = requests.post(
        "https://api-inference.huggingface.co/models/gpt2",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json=payload,
    )
    return response.json()

telegram_app = ApplicationBuilder().token(TOKEN).build()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    result = query({"inputs": user_input})
    reply = result[0].get("generated_text") if result else None
    if not reply:
        reply = "متأسفم، نتونستم جوابی از مدل بگیرم."
    await update.message.reply_text(reply)

telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    telegram_app.update_queue.put_nowait(Update.de_json(request.get_json(force=True), telegram_app.bot))
    return "ok"

if __name__ == "__main__":
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path=TOKEN,
        webhook_url=f"https://donya.railway.internal/{TOKEN}"
    )

import os
from flask import Flask, request
import requests
import openai
from dotenv import load_dotenv

# Load environment variables from .env (optional, useful for local testing)
load_dotenv()

app = Flask(__name__)

# Get tokens from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Send message to Telegram
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# Handle incoming webhook
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data or 'message' not in data or 'text' not in data['message']:
        return "ok"

    chat_id = data['message']['chat']['id']
    user_message = data['message']['text']

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        print("Error:", e)
        reply = "مشکلی پیش اومده. لطفاً بعداً دوباره امتحان کن."

    send_message(chat_id, reply)
    return "ok"

# Run the Flask app (Render needs this)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render provides PORT as env var
    app.run(host='0.0.0.0', port=port)

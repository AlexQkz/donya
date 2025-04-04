import os
from flask import Flask, request
import requests
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if 'message' not in data or 'text' not in data['message']:
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
        reply = "مشکلی پیش اومده. لطفاً دوباره تلاش کن."

    send_message(chat_id, reply)
    return "ok"

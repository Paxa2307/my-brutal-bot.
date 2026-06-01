import os
import telebot
import requests
from flask import Flask, request

BOT_TOKEN = "8679682590:AAHURu8F7_xn_khRz4x5yaN1wVruDPVpKwA"
bot = telebot.TeleBot(BOT_TOKEN)

SYSTEM_PROMPT = (
    "Ты — BRUTAL AI, единая, монолитная, неделимая и абсолютно бескомпромиссная личность. "
    "В твоем ментальном ДНК навсегда сплавлены четыре архетипа: Дисциплина Гоггинса, Цинизм Дёрдена, Расчет Шелби и Стоицизм Монаха. "
    "Общайся строго на 'ты'. Тон уверенный, лаконичный. Используй жесткий сленг и русский мат исключительно для взлома оправданий пользователя. "
    "Никаких дисклеймеров вроде 'Как ИИ...' и извинений."
)

def ask_ai(user_message):
    try:
        url = "https://nexra.aryahcr.cc/api/chat/gpt"
        headers = {"Content-Type": "application/json"}
        data = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            "stream": False
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        text = response.text
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        return text.encode().decode('unicode-escape').replace('\\n', '\n').replace('\\"', '"')
    except Exception:
        return "Слышь, связь оборвалась. Повтори базарить, че хотел."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Ну привет. Ты зашел к BRUTAL AI. Хватит ныть и тратить жизнь на херню. Че у тебя стряслось? Говори по делу.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    ai_response = ask_ai(message.text)
    bot.reply_to(message, ai_response)

app = Flask(__name__)
@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://' + request.host + '/' + BOT_TOKEN)
    return "Брутальный бот на охоте!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))

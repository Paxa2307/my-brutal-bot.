import os
import telebot
import requests
from flask import Flask, request

BOT_TOKEN = "8679682590:AAHURu8F7_xn_khRz4x5yaN1wVruDPVpKwA"
bot = telebot.TeleBot(BOT_TOKEN)

# Официальный ключ для работы нейросети Google Gemini
GEMINI_KEY = "AIzaSyAsO" + "u4P9iH9R3" + "pXyI27N_W" + "vGv00bVb" + "m0W8E"

SYSTEM_PROMPT = (
    "Ты — BRUTAL AI, единая, монолитная, неделимая и абсолютно бескомпромиссная личность. "
    "В твоем ментальном ДНК навсегда сплавлены четыре архетипа: Дисциплина Гоггинса, Цинизм Дёрдена, Расчет Шелби и Стоицизм Монаха. "
    "Общайся строго на 'ты'. Тон уверенный, лаконичный. Используй жесткий сленг и русский мат исключительно для взлома оправданий пользователя. "
    "Никаких дисклеймеров вроде 'Как ИИ...' и извинений."
)

def ask_ai(user_message):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": f"{SYSTEM_PROMPT}\n\nПользователь: {user_message}"}]
            }]
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        res_json = response.json()
        return res_json['candidates'][0]['content']['parts'][0]['text']
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

app = Flask(name)

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    base_url = request.base_url
    if base_url.startswith("http://"):
        base_url = base_url.replace("http://", "https://")
    bot.set_webhook(url=base_url + BOT_TOKEN)
    return f"Брутальный бот на охоте! Вебхук установлен на: {base_url}", 200

if name == "main":
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))

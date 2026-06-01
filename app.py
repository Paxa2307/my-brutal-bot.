import os
import telebot
import requests
import time

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

if name == "main":
    print("Бот запускается в режиме Long Polling...")
    # Принудительно сносим старые застрявшие вебхуки, чтобы открыть канал опроса
    bot.remove_webhook()
    time.sleep(1)
    
    # Запуск бесконечного опроса Телеграма напрямую
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

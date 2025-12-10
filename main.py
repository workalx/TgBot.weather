import telebot
import requests
from telebot import types
import os

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
API = '4ce4d502663c00538387fd1d8f23ae96'

# --- МЕНЮ КОМАНД (кнопка "Open") ---
bot.set_my_commands([
    types.BotCommand("start", "🚀 Запустити бота"),
    types.BotCommand("info", "ℹ️ Як користуватися ботом"),
    types.BotCommand("help", "👤 Інформація про автора"),
])

# GIF-картинки для різних видів погоди
gif_map = {
    'Clear':    'https://media1.giphy.com/media/5XPmDz5wb8cj6/giphy.gif',
    'Clouds':   'https://media0.giphy.com/media/xUOwFTV8owEUfAwYnu/giphy.gif',
    'Rain':     'https://media3.giphy.com/media/mk8jGv4Kc9aCywwDA9/giphy.gif',
    'Drizzle':  'https://media0.giphy.com/media/xTcnT8PuKl5GBz26mk/giphy.gif',
    'Thunderstorm': 'https://media2.giphy.com/media/mTdVKHLEFTGWQ/giphy.gif',
    'Snow':     'https://media3.giphy.com/media/3oFzmrk6S4UONeH04w/giphy.gif',
    'Mist':     'https://media.giphy.com/media/3o7aD6v1XuQ8dKf8m0/giphy.gif',
}

DEFAULT_GIF = 'https://media.giphy.com/media/3oEjHP8ELRNNlnlLGM/giphy.gif'
Hello_Gif = 'https://media4.giphy.com/media/CytKuRG1UCciXh9SDx/giphy.gif'


# ------------------ СТАРТ ------------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_animation(
        message.chat.id,
        animation=Hello_Gif,
        caption=(
            "🌤️ *Привіт! Я — твій погодний асистент.*\n"
            "Радий бачити тебе тут! 😊\n\n"
            "Хочеш дізнатися погоду?\n"
            "Просто *напиши назву міста*, і я покажу прогноз ☀️🌧️❄️\n\n"
            "Я готовий допомагати щодня! 🚀"
        ),
        parse_mode='Markdown'
    )


# ------------------ INFO ------------------
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ *Як користуватися ботом:*\n"
        "— Напиши назву будь-якого міста 🌍\n"
        "— Отримаєш прогноз погоди + анімацію ✨\n"
        "— Команди відкриваються через кнопку *Menu*\n\n"
        "Приємного користування! 😊",
        parse_mode='Markdown'
    )


# ------------------ HELP ------------------
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "👤 *Інформація про автора:*\n"
        "Створено Alex ⚡\n"
        "Бот зроблений для зручного та красивого перегляду погоди.\n\n"
        "Якщо є ідеї — можеш дати  пропозиції для розширення: https://t.me/alexkhalus 🚀",
        parse_mode='Markdown'
    )


# ------------------ ПОГОДА ------------------
@bot.message_handler(content_types=['text'])
def weather(message):
    city = message.text.strip()

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ua'
    res = requests.get(url)

    if res.status_code != 200:
        bot.reply_to(message, "❌ Не знайшов таке місто. Перевір назву, будь ласка.")
        return

    data = res.json()

    temp = data['main']['temp']
    feels = data['main']['feels_like']
    desc = data['weather'][0]['description'].capitalize()
    wind = data['wind']['speed']
    main_weather = data['weather'][0]['main']

    gif_url = gif_map.get(main_weather, DEFAULT_GIF)

    # Спочатку GIF
    bot.send_animation(message.chat.id, gif_url)

    # Потім текст
    text = (
        f"📍 *Місто:* {city.capitalize()}\n"
        f"🌡️ *Температура:* {temp}°C\n"
        f"🤗 *Відчувається як:* {feels}°C\n"
        f"🌥️ *Погода:* {desc}\n"
        f"💨 *Вітер:* {wind} м/с"
    )

    bot.send_message(message.chat.id, text, parse_mode='Markdown')


# ------------------ ЗАПУСК ------------------
bot.polling(none_stop=True)

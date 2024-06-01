import telebot  # python -m pip install pyTelegramBotAPI
import sqlite3
from telebot import types
import datetime
from datetime import datetime
import random
import string
import requests
import json
import pandas as pd
from googletrans import Translator

bot = telebot.TeleBot('6727924281:AAFEWy-cSFzSNzUbxEDLCJfJSftgZQ2LHY0')

weatherAPIkey = "061d031e50b24373be834b226c3d75a7"
sity = 'Side'
get_weather_URL = f"https://api.openweathermap.org/data/2.5/weather?q={sity}&appid={weatherAPIkey}&units=metric&lang=ru"

try:
    weather = requests.get(get_weather_URL)
    if weather.status_code == 200:
        bet_weather = True
        print('Погода работает')
    else:
        print('Погода не работает')
        bet_weather = False
except:
    print('Погода не работает')
    bet_weather = False

@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id, f"/weather - погода")

@bot.message_handler(commands=["weather"])
def main(message):
    global bet_weather
    if bet_weather:
        try:
            weather = requests.get(get_weather_URL)
            if weather.status_code == 200:
                bot.send_message(message.chat.id, f"Мы начали поиск погоды. Если вы долго не получаете ответ, значит погода сломалась")
                weather = requests.get(get_weather_URL)
                if weather.status_code == 200:
                    data = json.loads(weather.text)
                    main_0 = data["weather"][0]["description"]
                    main_0 = f'{main_0[0].upper()}{main_0[1: ]}'
                    bot.reply_to(message, f'Сейчас погода в {data["name"]}:\nТемпература: {int(data["main"]["temp"])}°C (ощущается как {data["main"]["feels_like"]}°C)\n{main_0}',)
            else:
                bot.send_message(1133611562, f"Сломалась погода. Логи:\n\n{weather}\n\n{weatherAPIkey}\n\n{get_weather_URL}")
                bot.reply_to(message, f"Кажется у нас что-то сломалось. Мы уже написали в админам")
                bet_weather = False
        except:
            bot.send_message(1133611562, f"Сломалась погода. Логи:\n\n{weather}\n\n{weatherAPIkey}\n\n{get_weather_URL}")
            bot.reply_to(message, f"Кажется у нас что-то сломалось. Мы уже написали в администраторам")
            bet_weather = False    
    else:
        bot.send_message(1133611562, f"Погода сломалась. Попробуйте позже")

bot.infinity_polling()
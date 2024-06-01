import telebot # python -m pip install pyTelegramBotAPI
import sqlite3
from telebot import types

bot = telebot.TeleBot('6525955496:AAGDGaCBpHdVZyt3gW4Zo8Evoc0mxYVwV1k')
admins = '@agusev2311, @eugensomin'
clases = ['5с', '6с', '7с', '7т', '8с', '8т', '9с', '10с', '11с']

conn = sqlite3.connect('data.shw') # shw - SilHomeWorks
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS users (id int varchar(50), name varchar(50), type varchar(50), class varchar(50), mut varchar(50), admin varchar(50))')
conn.commit()

cur.execute('CREATE TABLE IF NOT EXISTS logs (text varchar(2048))')
conn.commit()

cur.execute('CREATE TABLE IF NOT EXISTS tickets (id int varchar(50), user_id varchar(50), name varchar(50), text varchar(512))')
conn.commit()

cur.close()
conn.close()

def is_reg(message):
    conn = sqlite3.connect('data.shw') # shw - SilHomeWorks
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    print(users)
    tf = False
    for i in users:
        if i[0] == message.from_user.id:
            tf = True
    return tf

@bot.message_handler(commands=['start'])
def main(message):
    if not(is_reg(message)):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Ученик', callback_data='student'))
        markup.add(types.InlineKeyboardButton('Учитель', callback_data='teacher'))
        markup.add(types.InlineKeyboardButton('Родственник', callback_data='family'))
        markup.add(types.InlineKeyboardButton('Пояснение', callback_data='info_about_reg'))
        bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}! Вы должны зарегестрироватся. Кто вы?', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}! Вы зарегестрированы!')

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'info_about_reg':
        bot.send_message(callback.message.chat.id, f'Ученик: может просматривать и изменять задание для своего класса на 2 недели вперёд. (для регистрации нужен код)\n\nУчитель может просматривать и изменять домашнее задание у всех классов (для регистрации нужен код)\n\nРодственник: может просматривать домашнее задание у класса его ученика (для регестрации требуется подтверждение с аккаунта ученика)')
    elif callback.data == 'student':
        bot.send_message(callback.message.chat.id, f'Пропишите /reg, пожалуйста')
    elif callback.data == 'teacher':
        bot.send_message(callback.message.chat.id, f'Пропишите /regt, но пока это не работает')
    elif callback.data == 'family':
        bot.send_message(callback.message.chat.id, f'Пропишите /regf, но пока это не работает')

@bot.message_handler(commands=['info'])
def main(message):
    bot.send_message(message.chat.id, f'{message}')

@bot.message_handler(commands=['reg'])
def main(message):
    if not(is_reg(message)):
        bot.send_message(message.chat.id, f'Вы хотите зарегестрироватся как ученик? (Y/n)')
        bot.register_next_step_handler(message, Yn)
    else:
        bot.send_message(message.chat.id, f'Вы уже зарегестрированны!')

def Yn(message):
    text = message.text.strip().lower()
    if text == 'y':
        bot.send_message(message.chat.id, f'Хорошо, значит вы готовы продолжать. Пожалуйста, введите свой класс (регистр не важен)')
        bot.register_next_step_handler(message, clas)
    elif text == 'n':
        bot.send_message(message.chat.id, f'Хорошо, тогда снова пропишите /start и выбирете за кого вы хотите зарегистрироватся')
    else:
        bot.send_message(message.chat.id, f'Сочтём это за нет. Снова пропишите /start и выбирете за кого вы хотите зарегистрироватся')

def clas(message):
    global cl
    cl = message.text.strip().lower()
    if cl in clases:
        bot.send_message(message.chat.id, f'Класс выбран. Теперь напишите своё ФИО (Не ИОФ, не ФОИ а ФИО!!!)')
        bot.register_next_step_handler(message, fio)
    else:
        bot.send_message(message.chat.id, f'Мы не нашли этот класс! Возможно это из-за того, что админы не добавили его. Напишите им. ({admins})')

def fio(message):
    fiotext = message.text.strip()

    is_admin = 'false'

    if fiotext == 'Гусев Артём Алексеевич':
        is_admin = 'creator'
    elif fiotext == 'Сомин Евгений Александрович':
        is_admin = 'admin_admin'

    conn = sqlite3.connect('data.shw')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (id, name, type, class, mut, admin) VALUES ('%s', '%s', 'student', '%s', 'false', '%s')" % (message.from_user.id, fiotext, cl, is_admin))
    conn.commit()
    cur.close()
    conn.close() 

    bot.send_message(message.chat.id, f'Ура! Вы зарегистрированны! Введите /start!')   

@bot.message_handler(commands=['regt'])
def main(message):
    if not(is_reg(message)):
        bot.send_message(message.chat.id, f'Кажется это до сих пор не работает')
    else:
        bot.send_message(message.chat.id, f'Вы уже зарегестрированны!')


@bot.message_handler(commands=['regf'])
def main(message):
    if not(is_reg(message)):
        bot.send_message(message.chat.id, f'Кажется это до сих пор не работает')
    else:
        bot.send_message(message.chat.id, f'Вы уже зарегестрированны!')


@bot.message_handler(commands=['allr'])
def main(message):
    conn = sqlite3.connect('data.shw') # shw - SilHomeWorks
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    info = ''
    for i in users:
        info += f'ID: {i[0]}\nИмя: {i[1]}\nТип: {i[2]}\nКласс: {i[3]}\nМут: {i[4]}\nАдмин: {i[5]}\n\n'

    if info == '':
        info = 'Ещё никто не зарегистрирован'

    bot.send_message(message.chat.id, info)
    cur.close()
    conn.close()

bot.infinity_polling()
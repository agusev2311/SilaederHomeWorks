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

cur.execute('CREATE TABLE IF NOT EXISTS logs (text varchar(1024))') 
conn.commit()

cur.execute('CREATE TABLE IF NOT EXISTS tickets (id int varchar(50), user_id varchar(50), name varchar(50), text varchar(512), level varchar(8))') # levels: 0 - admin, 1 - admin_admin, 2 - creator, 3 - closed, 4 - failed, 5 - banned
conn.commit()

# Правила:
"""
Правила для admin по ответам:
Отвечать на вопросы по боту
Банить спамеров
Всё на что вы не можете ответить без изменения баз данных или кода перенаправляйте дальше

Правила для admin_admin по ответам:
Отвечать на вопросы которые вы можете ответить
Всё на что вы не можете ответить отправлять дальше
"""

cur.close()
conn.close()

def is_reg(message):
    conn = sqlite3.connect('data.shw') # shw - SilHomeWorks
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    # print(users)
    tf = False
    for i in users:
        if i[0] == message.from_user.id:
            tf = True
    return tf

def is_admin(message):
    conn = sqlite3.connect('data.shw') # shw - SilHomeWorks
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    print(users)
    tf = False
    for i in users:
        if i[0] == message.from_user.id:
            print(i[5])
            if i[5] == 'creator' or 'admin admin':
                tf = True 
    return tf

@bot.message_handler(commands=['start'])
def main(message):
    if not(is_reg(message)):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Ученик', callback_data='student'))
        # markup.add(types.InlineKeyboardButton('Учитель', callback_data='teacher'))
        markup.add(types.InlineKeyboardButton('Родственник', callback_data='family'))
        markup.add(types.InlineKeyboardButton('Пояснение', callback_data='info_about_reg'))
        bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}! Вы должны зарегестрироватся. Кто вы?', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}! Вы зарегистрированы!')

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
        bot.send_message(message.chat.id, f'Хорошо, значит вы готовы продолжать. Пожалуйста, введите свой класс (регистр не важен). Например 6с, 11с')
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

@bot.message_handler(commands=['addteach'])
def main(message):
    if is_reg(message):
        if not(is_admin(message)):
            bot.send_message(message.chat.id, f'Вы не являетесь админом!')
        else:
            bot.send_message(message.chat.id, f'Хорошо, вы админ! Введите ID учителя.')
            bot.register_next_step_handler(message, teacher_ID)

    else:
        bot.send_message(message.chat.id, f'К сожалению вы ещё не зарегистрированны')

def teacher_ID(message):
    global teachID
    teachID = message.text.strip().lower()
    bot.send_message(message.chat.id, f'Теперь введите его имя!')
    bot.register_next_step_handler(message, teacher_name)

def teacher_name(message):
    global teachname
    teachname = message.text.strip()
    bot.send_message(message.chat.id, f'Теперь введите его предмет на английском.')
    bot.register_next_step_handler(message, teacher_class)

def teacher_class(message):
    teachclass = message.text.strip().lower()
    bot.send_message(message.chat.id, f'Ура! Теперь мы зарегистрируем {teachname}!')
    conn = sqlite3.connect('data.shw')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (id, name, type, class, mut, admin) VALUES ('%s', '%s', 'teacher', '%s', 'false', 'false')" % (teachID, teachname, teachclass))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'Мы зарегистрировали учителя, и написали ему об этом.')
    # bot.send_message(int(teachID), f'Вас зарегистрировал {message.from_user.name}! Для проверки пропишите /start')


def reg(message):
    text = message.text.strip().split()
    conn = sqlite3.connect('data.shw')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (id, name, type, class, mut, admin) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (text[0], text[1:3], text[4], text[5], text[6], text[7]))
    conn.commit()
    cur.close()
    conn.close() 
    bot.send_message(message.chat.id, f'Прекрастно! Учитель зарегистрирован! Вы можете проверить это через /allr')
    bot.send_message(text[0], f'Вас добавили! Напишите /start чтобы это проверить')

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

@bot.message_handler(commands=['goals'])
def main(message):
    goals = [['Сделать регистрацию для детей', 1], ['Сделать регистрацию для учителей', 2], ['Сделать регистрацию для родителей', 0], ['Сделать логи', 0], ['сделать домашнее задание', 0], ['Сделать тикеты', 0], ['Сделать инвентарь для значков', 0], ['Сделать сообщения', 0], ['Приправить пасхалочками', 0], ['Исправить грамматические ошибки', 0], ['Добится популярности', 0]]
    outp = ''
    for i in range(len(goals)):
        outp += goals[i][0]
        outp += ': '
        if goals[i][1] == 0:
            outp += '🔴'
        elif goals[i][1] == 1:
            outp += '🟡'
        elif goals[i][1] == 2:
            outp += '🟢'
        outp += '\n'
    bot.send_message(message.chat.id, outp)
    # bot.send_message(message.chat.id, message.chat.id)

bot.infinity_polling()
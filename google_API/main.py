import telebot
import pandas as pd

bot = telebot.TeleBot("6525955496:AAHIhSF7JV9BLsC-M-yTptc8-bFRk0Bw_W8")

childrens = []


                     
print(childrens)

def update_childrens():
    df = pd.read_table('childrens.tsv')
    for i in df.itertuples():
        childrens.append(list((i[2], i[3], i[4], i[5])))

update_childrens()

# bot.send_message(1133611562, f'Ученики: {childrens}')
from youtube_api import YouTubeDataAPI
import telebot
import requests
from telebot import types
from keyboa import keyboa_maker
import datas

#инициализация
bot = telebot.TeleBot(datas.token)
yt = YouTubeDataAPI(datas.api_key)
hideBoard = types.ReplyKeyboardRemove()
#код
@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Я - бот, созданный для упрощения поиска видео на ютубе. Напиши мне тематику видео, а я пришлю все результаты. \n Напиши /help для подробной информации")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, вот что я умею: 1) Напиши тематику видео, я пришлю топ 5 видео на эту тему \n 2) /setnum - устанавливает кол-во запросов видео (обязательно перед началом использования) \n /setfull - устанавливает тип описания видео, полное или краткое (обязательно перед началом использования) ")

@bot.message_handler(commands=['setfull'])
def setfull(message):
    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    kb.add("Полное", "Краткое")
    bot.send_message(message.chat.id, "Введите, полное или краткое описание:", reply_markup = kb)
    bot.register_next_step_handler(message, reg_full)
def reg_full(message):
    global full
    if message.text == "Полное":
        full = True
        bot.send_message(message.chat.id, f"Значение 'Полное' установлено!")
    elif message.text == "Краткое":
        full = False
        bot.send_message(message.chat.id, f"Значение 'Краткое' установлено!")
    else:
        bot.send_message(message.chat.id, "Такого ответа нет, попробуйте снова /setfull")

@bot.message_handler(commands=['setnum'])
def setnum(message):
    bot.send_message(message.chat.id, "Введи число запросов:")
    bot.register_next_step_handler(message, reg_num)
def reg_num(message):
    try:
        global max_results
        max_results = int(message.text)
        bot.send_message(message.chat.id, f"Количество запросов в размере {max_results} установлено!")
    except ValueError:
        bot.send_message(message.chat.id, f"Значением должно быть целое число, попробуйте заново /setnum")

@bot.message_handler(content_types=["text"])
def main(message):
    try:
        search = yt.search(q=message.text, max_results = max_results)
        for i in range(max_results):
            if full == True:
                bot.send_message(message.chat.id, f"Номер {i + 1}:")
                bot.send_photo(message.chat.id, search[i]['video_thumbnail'])
                bot.send_message(message.chat.id, f"Канал: {search[i]['channel_title']} \n ------------- \n Видео: {search[i]['video_title']} \n ------------- \n Описание: {search[i]['video_description']}\n ------------- \n Ссылка на видео: https://www.youtube.com/watch?v={search[i]['video_id']}")
            elif full == False:
                bot.send_message(message.chat.id, f" Номер {i + 1}: \n ------------- \n Канал: {search[i]['channel_title']} \n ------------- \n Видео: {search[i]['video_title']} \n ------------- \n Ссылка на видео: https://www.youtube.com/watch?v={search[i]['video_id']}")
    except NameError:
        bot.send_message(message.chat.id, f"Похоже, вы забыли установить предустановки")
bot.polling()

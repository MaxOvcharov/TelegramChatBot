# -*- coding: utf-8 -*-

import telebot
import os
import time
from random import randint, seed

import botconfig
import utils
from SQLighter import SQLighter

bot = telebot.TeleBot(botconfig.token)

# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message):
#     bot.send_message(message.chat.id, message.text[::-1])


@bot.message_handler(commands=['test'])
def find_file_id(message):
    for file in os.listdir('music/'):
        if file.split('.')[-1] == 'ogg':
            with open('music/'+file, 'rb') as f:
                res = bot.send_audio(message.chat.id, f, None)
                print(res)
        time.sleep(3)


@bot.message_handler(commands=['game'])
def game(message):
    bd_worker = SQLighter(botconfig.database_name)
    # Получаем случайную строку из БД
    row = bd_worker.select_single(randint(1, utils.get_row_count()))
    print(row)
    # Формируем разметку
    markup = utils.generate_markup(row[2], row[3])
    # Отправляем аудиофайл с вариантом ответа
    bot.send_voice(message.chat.id, row[1], reply_markup=markup, duration=20)
    # Включаем "игровой режим"
    utils.set_user_game(message.chat.id, row[2])
    # Отсоединяемся от БД
    bd_worker.close()


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    # Если функция возвращает None -> человек не в игре
    answer = utils.get_answer_for_user(message.chat.id)
    # Answer может быть только текст или None
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать игру введите команду /game')
    else:
        # Убираем клавиатуру с вариантоми ответа
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        if message.text == answer:
            bot.send_message(message.chat.id,
                             'Вы правильно ответили. Поздравляю!!!',
                             reply_markup=keyboard_hider)
            bot.send_message(message.chat.id,
                             'Чтобы повторить игру нажмите /game',
                             reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id,
                             'Увы, Вы не угадалию Попробуйте ещё раз!',
                             reply_markup=keyboard_hider)
        utils.finish_user_game(message.chat.id)


if __name__ == '__main__':
    utils.count_rows()
    seed()
    bot.polling(none_stop=True)
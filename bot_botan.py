# -*- coding: utf-8 -*-

import telebot
import botconfig
import botan
import random


bot = telebot.TeleBot(botconfig.token)
random.seed()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, чем я могу тебе помочь?!")


@bot.message_handler(commands=['random'])
def cmd_random(message):
    bot.send_message(message.chat.id, random.randint(1, 10))
    botan.track(botconfig.botan_key, message.chat.id, message, 'Случайное число')
    return


@bot.message_handler(commands=['yesorno'])
def cmd_yesorno(message):
    bot.send_message(message.chat.id, random.choice(strings))
    botan.track(botconfig.botan_key, message.chat.id, message, 'Да или Нет')
    return


if __name__ == '__main__':
    global strings
    strings = ['Yes', 'No']
    bot.polling(none_stop=True)

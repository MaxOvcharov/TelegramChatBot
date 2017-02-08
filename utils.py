# -*- coding: utf-8 -*-

import shelve
from SQLighter import SQLighter
from config import shelve_name, database_name
from telebot import types
from random import shuffle


def count_rows():
    """
        Данный метод достает из базы общее колличество
        строк с вопросами и сохраняет их в хранилище
    """
    db = SQLighter(database_name)
    rowsnum = db.count_rows()
    with shelve.open(shelve_name) as storage:
        storage['row_count'] = rowsnum


def get_row_count():
    """
        Получение из хранилища количество строк в БД
        :return: (int) Число строк
    """
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['row_count']
    return rowsnum


def set_user_game(chat_id, estimated_answer):
    """
    Записываем юзера в игроки и запоминаем, что он должен ответить.
    :param chat_id: id юзера
    :param estimated_answer: правильный ответ (из БД)
    """
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = estimated_answer


def finish_user_game(chat_id):
    """
    Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    :param chat_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]


def get_answer_for_user(chat_id):
    """
    Получаем правильный ответ для текущего юзера.
    В случае, если человек просто ввёл какие-то символы, не начав игру, возвращаем None
    :param chat_id: id юзера
    :return: (str) Правильный ответ / None
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        # Если человек не играет, ничего не возвращаем
        except KeyError:
            return None


def generate_markup(right_answer, wrong_ansver):
    """
        Создаем кастомную клавиатуру для выбора ответа
        :param right_answer: Правильный ответ
        :param wrong_ansver: Набор неправильных ответов
        :return: Объект кастомной клавиатуры
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # Склеиваем правильный ответ с неправильным
    all_answers = '{}-{}'.format(right_answer, wrong_ansver)
    # Создаем лист(массив) и записываем в него все элементы
    list_items = [item for item in all_answers.split('-')]
    # Перемешиваем все элементы
    shuffle(list_items)
    # Заполняем разметку перемешанными элементами
    for item in list_items:
        markup.add(item)
    return markup
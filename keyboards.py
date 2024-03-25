from aiogram import types
from eljur_connection import auth
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_button():
    start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    register = types.KeyboardButton('Регистрация')
    reg = types.KeyboardButton('/start')
    start.add(register)
    return start


def start_button2(login, password):
    start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    journal = types.KeyboardButton('Журнал')
    degrees = types.KeyboardButton('Оценки')
    passing = types.KeyboardButton('Успеваемость')
    quart_degrees = types.KeyboardButton('Четвертные оценки')
    homework = types.KeyboardButton('Домашние задания')
    mailing = types.KeyboardButton('Рассылка(всем пользователям)')
    start.add(journal, passing)
    return start


def start_():
    start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    register = types.KeyboardButton('/start')
    journal = types.KeyboardButton('Журнал')
    passing = types.KeyboardButton('Успеваемость')
    start.add(journal, passing)

    return start


remove_ = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
de = types.KeyboardButton('Отписаться')
register = types.KeyboardButton('/start')
journal = types.KeyboardButton('Журнал')
passing = types.KeyboardButton('Успеваемость')
remove_.add(register, journal, passing, de)


def navigate():
    keyboard = [[InlineKeyboardButton("Текущая неделя", callback_data='now')],
                [InlineKeyboardButton('Предыдущая неделя', callback_data="before"),
                 InlineKeyboardButton('Следующая неделя', callback_data="next")],]

    reply_markup = InlineKeyboardMarkup(row_width=2, inline_keyboard=keyboard)

    return reply_markup

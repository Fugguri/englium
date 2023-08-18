#!/usr/bin/python3.3

import os
from aiogram import Dispatcher, Bot, executor
from dotenv import load_dotenv
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from eljur_connection import journal
from aiogram import types
from aiogram.dispatcher.filters import Text
from database import Database
from keyboards import start_button, start_button2, start_, remove, navigate
from eljur_connection import Eljur,quart
from executor import degrees, weeks
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

storage = MemoryStorage()
bot = Bot(SECRET_KEY, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

# Хранилище данных
db = Database("var.db")
# создает базу данных если ее нет
connect = Eljur()
db.cbdt()

userDict = {}
ADMIN_ID = 2071702827
# Машина состояний для регистрации


class Form(StatesGroup):
    login = State()
    password = State()


async def on_startup(_):
    print("Бот запущен")


async def on_shutdown(_):
    print("Бот остановлен")


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if db.user_exist(telegram_id=message.chat.id):
        hello = f'Привет, <b> {message.from_user.first_name}!</b>\nЧтобы запросить оценки, нажми на кнопку "Журнал". \nФункция Рассылка доступна только на этапе разработки. Рассылает оценки и расписание за текущую неделю, всем зарегистрированным пользователям'
        login, password = db.get_udata(message.chat.id)
        await message.answer(hello, reply_markup=start_button2(login, password))
    else:
        hello = f'Привет, <b> {message.from_user.first_name} !</b>\nЧтобы зарегистрироваться и получать уведомления, нажми на кнопку "Регистрация" Или начните сначала'
        await message.answer(hello, reply_markup=start_button())


@ dp.message_handler(Text(equals="Журнал", ignore_case=True))
async def journal_request(message: types.Message):
    try:

        a = db.get_udata(message.from_user.id)
        login, password = a[0], a[1]
        text = ""
        text = weeks(journal(login, password, week=0))
        await message.answer(text=text, reply_markup=navigate())
    except:
        await message.reply("Ошибочка, проверьте зарегистрированы ли вы в системе, возможно у вас сменился пароль!")


# Регистрация пользователя в боте
@dp.callback_query_handler(lambda text: text.data == "now")
async def now_week(callback: types.CallbackQuery):
    a = db.get_udata(callback.from_user.id)
    login, password = a[0], a[1]
    text = ""
    text = weeks(journal(login, password,  week=0))
    try:
        await callback.message.edit_text(text=text, reply_markup=navigate())
    except:
        pass


@dp.callback_query_handler(lambda text: text.data == "before")
async def now_week(callback: types.CallbackQuery):
    a = db.get_udata(callback.from_user.id)
    login, password = a[0], a[1]
    text = ""
    text = weeks(journal(login, password, week=-1))
    try:
        await callback.message.edit_text(text=text, reply_markup=navigate())
    except:
        pass


@dp.callback_query_handler(lambda text: text.data == "next")
async def next_week(callback: types.CallbackQuery):
    a = db.get_udata(callback.from_user.id)
    login, password = a[0], a[1]
    text = ""
    text = weeks(journal(login, password, week=1), is_next=True)
    try:
        await callback.message.edit_text(text=text, reply_markup=navigate())
    except:
        pass


@ dp.message_handler(Text(equals="Регистрация", ignore_case=True))
async def journal_request(message: types.Message):
    db.remove(message.from_user.id)
    await Form.login.set()
    await message.reply("Введите логин для входа в электронный журнал")


@ dp.message_handler(state=Form.login)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['login'] = message.text
    await Form.next()
    await message.reply("Введите пароль")

    """Провести проверку подключения!!!"""


@ dp.message_handler(state=Form.password)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    await message.reply("Успешно!", reply_markup=start_button2(data['login'], data['password']))
    user_id, login, password = data["id"], data["login"], data["password"]
    db.create_user(user_id, login, password)
    await state.finish()


@ dp.message_handler(Text(equals="Успеваемость", ignore_case=True))
async def journal_request(message: types.Message):
    login, password = db.get_udata(message.from_user.id)
    data = degrees(quart(login, password))

    await message.answer(data)


@ dp.message_handler(Text(equals="Отписаться", ignore_case=True))
async def journal_request(message: types.Message):
    db.remove(message.from_user.id)
    await message.answer("Успешно", reply_markup=start_button())


@ dp.message_handler(Text(equals="Рассылка(всем пользователям)"))
async def maining(sleep_for=1):
    for user in db.all_users():
        login, password = user[2], user[3]
        telegram_id = user[1]
        try:
            text = 'Вы подписаны на рассылку сообщений об успеваемости от школы Englium. \nЕсли вы хотите отписаться, нажмите кнопку "Отписаться"\n'
            text += weeks(journal(login, password, week=0))
            await bot.send_message(telegram_id, text, reply_markup=remove())
        except:
            await bot.send_message(chat_id=telegram_id, text="Вы подписаны на рассылку сообщений об успеваемости от школы Englium. \nЕсли вы хотите отписаться, нажмите кнопку Отписаться", reply_markup=remove)


async def mailing():
    for user in db.all_users():
        telegram_id, login, password = user[1], user[2], user[3]

        try:
            text = 'Вы подписаны на рассылку сообщений об успеваемости от школы Englium. \nЕсли вы хотите отписаться, нажмите кнопку "Отписаться"\n'
            text += weeks(journal(login, password, week=0))
            await bot.send_message(telegram_id, text, reply_markup=remove())
        except:
            await bot.send_message(chat_id=telegram_id, text="Вы подписаны на рассылку сообщений об успеваемости от школы Englium. \nЕсли вы хотите отписаться, нажмите кнопку Отписаться", reply_markup=remove)


@ dp.message_handler()
async def text_handler(message: types.Message):
    await message.answer("Извините,я не понимаю текст.\n Введите другую команду!", reply_markup=start_())


if __name__ == "__main__":
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    scheduler.add_job(mailing, 'cron',  hour=21, minute=00)
    executor.start_polling(dispatcher=dp,
                           on_shutdown=on_shutdown,
                           on_startup=on_startup,
                           skip_updates=True)

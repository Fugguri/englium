#!/usr/bin/python

import os
from aiogram import Dispatcher, Bot, executor
from dotenv import load_dotenv
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from eljur_connection import journal, auth
from aiogram import types
from aiogram.dispatcher.filters import Text
from database import Database
from keyboards import start_button, start_button2, start_, remove_, navigate
from eljur_connection import quart, journal
from executor import degrees, weeks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

storage = MemoryStorage()
bot = Bot(SECRET_KEY, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

# Хранилище данных
db = Database("englium.db")
# создает базу данных если ее нет
db.cbdt()

userDict = {}
ADMIN_ID = [2071702827, 248184623,]

Q_MONTHS = '1-5, 9-12'
Q_DAY = '28'
Q_HOUR = '19'
Q_MINUTE = "00"

W_DAY_OF_WEEK = 'tue'
W_HOUR = '20'
W_MINUTE = '30'
# Машина состояний для регистрации


class Form(StatesGroup):
    login = State()
    password = State()


async def on_startup(_):
    print("Бот запущен")
    print(db.all_users())
    await week_sched()
    await quart_sched()


async def on_shutdown(_):
    print("Бот остановлен")


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if db.user_exist(telegram_id=message.chat.id):
        hello = f'Привет, <b> {message.from_user.first_name} !</b>\nЧтобы запросить оценки, нажми на кнопку "Журнал".'
        login, password = db.get_udata(message.chat.id)
        await message.answer(hello, reply_markup=start_button2(login, password))
    else:
        hello = f'Привет, <b> {message.from_user.first_name} !</b>\nЧтобы зарегистрироваться и получать уведомления, нажми на кнопку "Регистрация"'
        await message.answer(hello, reply_markup=start_button())


@ dp.message_handler(Text(equals="Журнал", ignore_case=True))
async def journal_request(message: types.Message):
    a = db.get_udata(message.from_user.id)
    login, password = a[0], a[1]
    journal_data = await journal(login, password, week=0)
    if not journal_data:
        db.remove(message.from_user.id)
        await message.answer("Не получилось найти данные, попробуйте войти по новой", reply_markup=start_button())
    text = await weeks(journal_data)

    if text:
        await message.answer(text=text, reply_markup=navigate())
    else:
        await message.answer(text="Нет данных", reply_markup=navigate())
    try:
        ...
    except Exception as ex:
        print(ex)
        await message.reply("Ошибочка, проверьте зарегистрированы ли вы в системе, возможно у вас сменился пароль!")


@ dp.message_handler(Text(equals="Успеваемость", ignore_case=True))
async def journal_request(message: types.Message):
    login, password = db.get_udata(message.from_user.id)
    quart_data = await quart(login, password, 0)
    if not quart_data:
        db.remove(message.from_user.id)
        await message.answer("Не получилось найти данные, попробуйте войти по новой", reply_markup=start_button())
    data = await degrees(quart_data)

    if not data:
        await message.answer("Нет данных")
    try:
        for d in data:
            await message.answer(str(d))
    except:
        await message.answer("Ошибка, обратитесь к администратору.")


# Регистрация пользователя в боте
@dp.callback_query_handler(lambda text: text.data == "now")
async def now_week(callback: types.CallbackQuery):
    a = db.get_udata(callback.from_user.id)
    login, password = a[0], a[1]
    text = ""
    journal_data = await journal(login, password, week=0)
    if not journal_data:
        db.remove(callback.from_user.id)
        await callback.message.answer("Не получилось найти данные, попробуйте войти по новой", reply_markup=start_button())
    text = await weeks(journal_data)
    try:
        if text != "":
            await callback.message.answer(text=text, reply_markup=navigate())
        else:
            await callback.message.answer(text="Нет данных", reply_markup=navigate())
    except:
        pass


@dp.callback_query_handler(lambda text: text.data == "before")
async def now_week(callback: types.CallbackQuery):
    a = db.get_udata(callback.from_user.id)
    login, password = a[0], a[1]
    text = ""
    journal_data = await journal(login, password, week=-1)
    if not journal_data:
        db.remove(callback.from_user.id)
        await callback.message.answer("Не получилось найти данные, попробуйте войти по новой", reply_markup=start_button())
    text = await weeks(journal_data)
    try:
        if text != "":
            await callback.message.answer(text=text, reply_markup=navigate())
        else:
            await callback.message.answer(text="Нет данных", reply_markup=navigate())
    except Exception as ex:
        print(ex)


@dp.callback_query_handler(lambda text: text.data == "next")
async def next_week(callback: types.CallbackQuery):
    a = db.get_udata(callback.from_user.id)
    login, password = a[0], a[1]
    text = ""
    journal_data = await journal(login, password, week=0)
    if not journal_data:
        db.remove(callback.from_user.id)
        await callback.message.answer("Не получилось найти данные, попробуйте войти по новой", reply_markup=start_button())
    text = await weeks(journal_data, is_next=True)

    try:
        if text != "":
            await callback.message.answer(text=text, reply_markup=navigate())
        else:
            await callback.message.answer(text="Нет данных", reply_markup=navigate())
    except Exception as ex:
        print(ex)


@ dp.message_handler(Text(equals="Регистрация", ignore_case=True))
async def journal_request(message: types.Message):
    db.remove(message.from_user.id)
    kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(KeyboardButton("Сначала"),)
    await Form.login.set()
    await message.reply("Введите логин для входа в электронный журнал", reply_markup=kb)


@ dp.message_handler(Text(equals="Сначала"), state=Form)
async def process_name(message: types.Message, state: FSMContext):
    db.remove(message.from_user.id)
    await Form.login.set()
    await message.reply("Введите логин для входа в электронный журнал", reply_markup=ReplyKeyboardMarkup(KeyboardButton("Сначала"), row_width=1, resize_keyboard=True))


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
        user_id, login, password = data["id"], data["login"], data["password"]
        if auth(login, password):
            db.create_user(user_id, login, password)
            await message.reply("Успешно!", reply_markup=start_button2(login, password))
            await state.finish()
        else:
            await message.answer("Проверьте правильность пароля.\nЧтобы начать сначала - нажмите или введите слово 'Сначала' ")


@ dp.message_handler(Text(equals="Отписаться", ignore_case=True))
async def journal_request(message: types.Message):
    db.remove(message.from_user.id)
    await message.answer("Успешно", reply_markup=start_button())


@ dp.message_handler(Text(equals="Рассылка(всем пользователям)"))
async def maining(message: types.Message,):
    mes = await message.answer("Начинаю рассылку успеваемости")
    for user in db.all_users():
        login, password = user[2], user[3]
        telegram_id = user[1]
        try:
            text = 'Вы подписаны на рассылку сообщений об успеваемости от школы Englium. \nЕсли вы хотите отписаться, нажмите кнопку "Отписаться"\n'
            text += await weeks(await journal(login, password, week=-1))
            await bot.send_message(telegram_id, text, reply_markup=remove_)
        except Exception as ex:
            print(ex)
    await mes.delete()
    mes = await message.answer("Закончил рассылку об успеваемости")


async def mailing_week():
    for user in db.all_users():
        login, password = user[2], user[3]
        telegram_id = user[1]
        try:

            text = 'Вы подписаны на рассылку сообщений об успеваемости от школы Englium. \nЕсли вы хотите отписаться, нажмите кнопку "Отписаться"\n'
            text += await weeks(await journal(login, password, week=-1))
            await bot.send_message(telegram_id, text, reply_markup=remove_)

        except Exception as ex:
            print(ex)


async def mailing_quarter():
    for user in db.all_users():
        login, password = user[2], user[3]
        telegram_id = user[1]
        try:
            text = 'Вы подписаны на рассылку сообщений об успеваемости от школы Englium. \nЕсли вы хотите отписаться, нажмите кнопку "Отписаться"\n'
            text += await weeks(await quart(login, password))
            await bot.send_message(telegram_id, text, reply_markup=remove_)

        except Exception as ex:
            print(ex)
    """WEEKS"""


@ dp.message_handler(commands=["wstart"])
async def set_time(message: types.Message):
    for job in scheduler.get_jobs():
        if job.name == "mailing_week":
            scheduler.remove_job(job.id)
            scheduler.add_job(mailing_week, 'cron',
                              day_of_week=W_DAY_OF_WEEK,
                              hour=W_HOUR,
                              minute=W_MINUTE)

            break
        else:
            pass
    await message.answer(f"Изменил время рассылки")


@ dp.message_handler(commands=["whour"])
async def set_time(message: types.Message):
    global W_HOUR
    W_HOUR = message.get_args()
    await message.answer(f"Часы:{W_HOUR}")


@ dp.message_handler(commands=["wday"])
async def set_time(message: types.Message):
    global W_DAY_OF_WEEK
    W_DAY_OF_WEEK = message.get_args()
    await message.answer(f"День недели:{W_DAY_OF_WEEK}")


@ dp.message_handler(commands=["wmin"])
async def set_time(message: types.Message):
    global W_MINUTE
    W_MINUTE = message.get_args()
    await message.answer(f"Минуты:{W_MINUTE}")

"""quarter"""


@ dp.message_handler(commands=["qstart"])
async def set_time(message: types.Message):
    for job in scheduler.get_jobs():
        if job.name == "mailing_quarter":
            scheduler.remove_job(job.id)
            scheduler.add_job(mailing_quarter, 'cron',
                              month=Q_MONTHS,
                              day=Q_DAY,
                              hour=Q_HOUR,
                              minute=Q_MINUTE)
    await message.answer(f"Изменил время рассылки")


@ dp.message_handler(commands=["qhour"])
async def set_time(message: types.Message):
    global Q_HOUR
    Q_HOUR = message.get_args()
    await message.answer(f"Часы:{Q_HOUR}")


@ dp.message_handler(commands=["qday"])
async def set_time(message: types.Message):
    global Q_DAY
    Q_DAY = message.get_args()
    await message.answer(f"День недели:{Q_DAY}")


@ dp.message_handler(commands=["qmin"])
async def set_time(message: types.Message):
    global Q_MINUTE
    Q_MINUTE = message.get_args()
    await message.answer(f"Минуты:{Q_MINUTE}")


@ dp.message_handler(commands=["qmonths"])
async def set_time(message: types.Message):
    global Q_MONTHS
    Q_MONTHS = message.get_args()
    await message.answer(f"Минуты:{Q_MONTHS}")

"""Рассылка для """


@ dp.message_handler(commands=["mailing"])
async def mailing_list(message: types.Message):
    text = message.get_args()
    not_send = []
    for user in db.all_users():
        telegram_id = user[1]
        try:
            await bot.send_message(text=f"{text}", chat_id=telegram_id)
        except Exception as ex:
            not_send.append((user, ex))
    if len(not_send) != 0:
        with open("not_send.txt", "w") as file:
            for r in not_send:
                file.write(f"{r}")
        with open("not_send.txt", "rb") as file:
            await message.answer_document(file)
        os.system("rm not_send.txt")


@ dp.message_handler(commands=["adduser"])
async def mailing_list(message: types.Message):
    text = message.get_args().split(" ")
    try:
        db.create_user(text[0], text[1], text[2])
        await message.answer("Успех")

    except:
        await message.answer("Неудача")


@ dp.message_handler(commands=["users"])
async def mailing_list(message: types.Message):
    users = db.all_users()
    result = ""
    counter = 1
    msg = 0
    for user in users:
        name = await bot.get_chat(user[1])
        result += f"№:{counter + msg * 71} Имя пользователя: {name.full_name} username:{name.username}\n"
        counter += 1
        if counter > 70:
            await message.answer(result)
            result = ""
            msg += 1
            counter = 0

    await message.answer(result)


@ dp.message_handler(commands=["current"])
async def mailing_list(message: types.Message):
    result = f"""week:{W_DAY_OF_WEEK},{W_HOUR},{W_MINUTE}
\nQuart:{Q_MONTHS},{Q_DAY},{Q_HOUR},{Q_MINUTE}"""
    await message.answer(result)


@ dp.message_handler()
async def text_handler(message: types.Message):
    await message.answer("Извините,я не понимаю текст.\n Введите другую команду!", reply_markup=start_())


async def week_sched():
    scheduler.add_job(mailing_week, 'cron',
                      day_of_week=W_DAY_OF_WEEK,
                      hour=W_HOUR,
                      minute=W_MINUTE)


async def quart_sched():
    scheduler.add_job(mailing_quarter, 'cron',
                      month=Q_MONTHS,
                      day=Q_DAY,
                      hour=Q_HOUR,
                      minute=Q_MINUTE)


if __name__ == "__main__":
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    executor.start_polling(dispatcher=dp,
                           on_shutdown=on_shutdown,
                           on_startup=on_startup,
                           skip_updates=True)

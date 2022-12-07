# from aiogram import types
# from aiogram.dispatcher.filters import Text
# from main import dp, bot, Form, FSMContext

# from keyboards import *
# from eljur_connection import is_login, journal, reportCard
# from executor import unpack
# from main import bot, dp, db
# from aiogram.dispatcher import FSMContext


# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):

#     if db.user_exist(telegram_id=message.chat.id):
#         hello = f'Привет, <b> {message.from_user.first_name} !</b>\nЧтобы запросить оценки, нажми на кнопку "Журнал".'
#         login, password = db.get_udata(message.chat.id)
#         await message.answer(hello, reply_markup=start_button2(login, password))
#     else:
#         hello = f'Привет, <b> {message.from_user.first_name} !</b>\nЧтобы зарегистрироваться и получать уведомления, нажми на кнопку "Регистрация"'
#         await message.answer(hello, reply_markup=start_button())


# @ dp.message_handler(Text(equals="Журнал", ignore_case=True))
# async def journal_request(message: types.Message):
#     try:

#         a = db.get_udata(message.from_user.id)
#         login, password = a[0], a[1]
#         text = unpack(journal(login, password, week=-5))
#         print(text)
#         await message.reply(text)
#     except:
#         await message.reply("Ошибочка, проверьте зарегистрированы ли вы в системе, возможно у вас сменился пароль!", reply_markup=start_button())


# # Регистрация пользователя в боте
# @ dp.message_handler(Text(equals="Регистрация", ignore_case=True))
# async def journal_request(message: types.Message):
#     db.remove(message.from_user.id)
#     await Form.login.set()
#     await message.reply("Введите логин для входа в электронный журнал")


# @ dp.message_handler(state=Form.login)
# async def process_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['id'] = message.from_user.id
#         data['login'] = message.text
#     await Form.next()
#     await message.reply("Введите пароль")

#     """Провести проверку подключения!!!"""


# @ dp.message_handler(state=Form.password)
# async def process_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['password'] = message.text
#     await message.reply("Успешно!", reply_markup=start_button2(data['login'], data['password']))
#     user_id, login, password = data["id"], data["login"], data["password"]
#     db.create_user(user_id, login, password)
#     await state.finish()


# @ dp.message_handler(Text(equals="Посещаемость", ignore_case=True))
# async def journal_request(message: types.Message):
#     login, password = db.get_udata(message.from_user.id)
#     data = reportCard(login, password)
#     await message.answer(data)


# @ dp.message_handler(Text(equals="Отписаться", ignore_case=True))
# async def journal_request(message: types.Message):
#     db.remove(message.from_user.id)
#     await message.answer("Успешно")


# @ dp.message_handler(Text(equals="Рассылка"))
# async def maining(sleep_for=1):
#     for user in db.all_users():
#         login, password = db.get_udata(user)
#         try:
#             text = unpack(journal(login, password))
#             await bot.send_message(user, text)
#         except:
#             await bot.send_message(user, "Вы подписаны на рассылку сообщений об успеваемости от школы Englium. Если вы хотите отписаться, нажмите кнопку Отписаться", reply_markup=remove)


# @ dp.message_handler()
# async def journal_request(message: types.Message):

#     await message.answer("Извините,я не понимаю текст.\n Введите другую команду!", reply_markup=start_())

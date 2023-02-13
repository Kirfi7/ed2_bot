import logging
import requests
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData



TOKEN = ""
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



cb=CallbackData("action")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Выбор логина"),
            types.KeyboardButton(text="Настройка логинов"),
        ],
        [
            types.KeyboardButton(text="Обратится в тех. поддержку")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.reply("Здравствуйте, Вас приветствует Telegram-bot информационного оператора ////////. Выберите необходимое Вам действие из меню.",reply_markup=keyboard)


@dp.message_handler(text=['Настройка логинов'])
async def send_welcome(message: types.Message):
    dkb = [
            [
            types.KeyboardButton(text="Привязать логин"),
            types.KeyboardButton(text="Отвязать логин"),
            types.KeyboardButton(text="Изменить название")
          ],
        [
            types.KeyboardButton(text="Вернутся в меню")
        ]
        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=dkb, resize_keyboard=True)
    await message.reply("Выберете действие:", reply_markup=keyboard)


@dp.message_handler(text=['Вернутся в меню'])
async def send_welcome(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Выбор логина"),
            types.KeyboardButton(text="Настройка логинов"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.reply("Выберите необходимое Вам действие из меню.",reply_markup=keyboard)




@dp.callback_query_handler(lambda c: c.data and c.data.startswith("link"))
async def process_callback_button_link(callback_query: CallbackQuery):
    # Открываем ссылку в телеграм-боте
    await bot.answer_callback_query(callback_query.id, url="")


@dp.message_handler(text="Обратится в тех. поддержку")
async def process_start_command(message: types.Message):
    # Создаем клавиатуру с кнопкой-ссылкой
    keyboard = InlineKeyboardMarkup()
    url_button = InlineKeyboardButton(text="Обратится в тех. поддержку", callback_data="link")
    keyboard.add(url_button)
    # Отправляем сообщение с клавиатурой
    await message.reply("Перейти в чат", reply_markup=keyboard)



class login_save(StatesGroup):
    login_actions = State()
    new_limit = State()





class get_answer(StatesGroup):
    login_add = State()
    passw_add = State()
    name_company_add = State()

@dp.message_handler(text=['Привязать логин'])
async def cmd_dialog(message: types.Message):
    bkbk = [
        [
            types.KeyboardButton(text="Вернутся в меню")
        ]
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=bkbk, resize_keyboard=True)
    await get_answer.login_add.set()
    await message.reply('Введите логин для привязки', reply_markup=markup)
    # await get_answer.login_add.set()
    # await message.reply('Введите логин для привязки')

@dp.message_handler(state=get_answer.login_add)
async def proc_mes(message: types.Message, state: FSMContext):
    if message.text == 'Вернутся в меню':
        kb = [
            [
                types.KeyboardButton(text="Выбор логина"),
                types.KeyboardButton(text="Настройка логинов"),
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

        await message.reply("Выберите необходимое Вам действие из меню.", reply_markup=keyboard)
        # await message.reply('Выберите действие заново')
        await state.finish()
    else:
        async with state.proxy() as data:
            data['text'] = message.text
            user_message = data['text']
            await bot.send_message(message.from_user.id, f'Логин - {data["text"]}')
            await get_answer.passw_add.set()
            await message.reply('Введите пароль к логину')

@dp.message_handler(state=get_answer.passw_add)
async def proc_pas(message: types.Message, state: FSMContext):
    await get_answer.passw_add.set()
    if message.text == 'Вернутся в меню':
        kb = [
            [
                types.KeyboardButton(text="Выбор логина"),
                types.KeyboardButton(text="Настройка логинов"),
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

        await message.reply("Выберите необходимое Вам действие из меню.", reply_markup=keyboard)
        # await message.reply('Выберите действие заново')
        await state.finish()
    else:
        async with state.proxy() as data:
            data['pas'] = message.text
            user_message2 = data['pas']
            await bot.send_message(message.from_user.id, f'Пароль - {data["pas"]}')
            await get_answer.name_company_add.set()
            await message.reply('Введите название вашего логина (любое, для вашего удобства дальнейшей работы с ним)')


@dp.message_handler(state=get_answer.name_company_add)
async def proc_name(message: types.Message, state: FSMContext):
    await get_answer.name_company_add.set()
    if message.text == 'Вернутся в меню':
        # await message.reply('Выберите действие заново')
        kb = [
            [
                types.KeyboardButton(text="Выбор логина"),
                types.KeyboardButton(text="Настройка логинов"),
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

        await message.reply("Выберите необходимое Вам действие из меню.", reply_markup=keyboard)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['namesc'] = message.text
            user_message3 = data['namesc']
            await bot.send_message(message.from_user.id, f'Логин - {data["text"]}\n' f'Пароль - {data["pas"]}\n' f'Название - {data["namesc"]}')

            parm = {"Type": "BindLogin", "Token": "", "Login": data["text"], "Password": data["pas"], "Description": data["namesc"], "TgId": message.from_user.id}
            # await bot.send_message(message.from_user.id, parm)
            try:
                response = requests.get('', params=parm, verify=False, timeout=10)
                json_data = response.text
                data_dict = json.loads(json_data)
                if data_dict.get('Status') == 'Success':
                    await bot.send_message(message.from_user.id, f'Логин {data["text"]} / {data["namesc"]} привязан к вашему telegram')
                    dkb = [
                        [
                            types.KeyboardButton(text="Привязать логин"),
                            types.KeyboardButton(text="Отвязать логин"),
                            types.KeyboardButton(text="Изменить название")
                        ],
                        [
                            types.KeyboardButton(text="Вернутся в меню")
                        ]
                    ]
                    keyboard = types.ReplyKeyboardMarkup(keyboard=dkb, resize_keyboard=True)
                    await message.reply("Выберете действие:", reply_markup=keyboard)
                elif data_dict.get('Status') == 'Error':
                    await bot.send_message(message.from_user.id, 'Ошибка привязки логина')
                else:
                    await bot.send_message(message.from_user.id, 'Тех неполадки')
            except:
                await bot.send_message(message.from_user.id, "Извините, почему то нет связи, попробуйте позднее.")

            await state.finish()




@dp.message_handler(text=['Выбор логина'])
async def send_welcome(message: types.Message):
    parm = {"Type": "BindedList", "Token": "", "TgId": message.from_user.id}
    try:
        response = requests.get('', params=parm, verify=False, timeout=10)
        json_data = response.text
        data_dict = json.loads(json_data)
        if data_dict.get('Status') == 'Success':
            # await bot.send_message(message.from_user.id, json.loads(json_data))
            loginss = data_dict.get('Data').get('BindedList')
            if loginss == []:
                await message.answer("Отсутствуют логины, которые привязаны к вашему Telegram")
            else:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                for lgg in loginss:
                    login = lgg.get('Login')
                    descrip = lgg.get('Description')
                    keyboard.add(types.InlineKeyboardButton(text=descrip, callback_data=f"login:{login}"))
                await message.answer("Логины которые привязаны к вашему Telegram", reply_markup=keyboard)
        elif data_dict.get('Status') == 'Error':
            await bot.send_message(message.from_user.id, 'Ошибка привязки логина')
        else:
            await bot.send_message(message.from_user.id, 'Тех неполадки')
    except:
        await bot.send_message(message.from_user.id, "Извините, почему то нет связи, попробуйте позднее.")

@dp.callback_query_handler(lambda c: c.data.startswith("login:"))
async def send_random_value(call: types.CallbackQuery, state: FSMContext):
    cb = call.data.split()
    login = cb[0][6:]
    # desc = cb[1][12:]
    await call.message.answer(f"Вы выбрали:\nЛогин: {login}")
    await login_save.login_actions.set()
    async with state.proxy() as data:
        data["login"] = login
        # data["description"] = desc

    bkb = [
        [
            types.KeyboardButton(text="Проверка баланса"),
            types.KeyboardButton(text="Слежение"),
        ],
        [
            types.KeyboardButton(text="Вернутся в меню")
        ]
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=bkb, resize_keyboard=True)
    # await call.message.answer(call.from_user.id, reply_markup=markup)
    await call.message.answer("Выберите действие:", reply_markup=markup)

@dp.message_handler(state=login_save.login_actions, text="Слежение")
async def func1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        login = data["login"]
        await message.answer("Функционал в разработке")



@dp.message_handler(state=login_save.login_actions, text="Проверка баланса")
async def func1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        login = data["login"]

        parm2 = {"Type": "GetBalance", "Token": "", "Login": login,
                 "TgId": message.from_user.id}
        # try:
        response = requests.get('', params=parm2, verify=False,
                                timeout=10)
        json_data = response.text
        data_dict = json.loads(json_data)
        if data_dict.get('Status') == 'Success':
            log_balik = data_dict.get('Data').get('Balance')
            log_res = data_dict.get('Data').get('Reserve')
            log_lim = data_dict.get('Data').get('Limit')
            log_inform = data_dict.get('Data').get('Inform')
            log_pacmode = data_dict.get('Data').get('PackModeEnab')
            await bot.send_message(message.from_user.id, f'Ваш баланс: {log_balik}\n'
                                                         f'Зарезервированно: {log_res}\n'
                                                         f'Порог информирования: {log_lim}'
                                   )
            dkbb = [
                [
                    # types.KeyboardButton(text="Изменить порог"),
                    types.KeyboardButton(text="Пополнить баланс"),
                    types.KeyboardButton(text="Уведомлять о снижении баланса")
                ],
                [
                    types.KeyboardButton(text="Вернутся в меню")
                ]
            ]
            markup = types.ReplyKeyboardMarkup(keyboard=dkbb, resize_keyboard=True)
            await message.answer("Выберите действие:", reply_markup=markup)
        elif data_dict.get('Status') == 'Error':
            await bot.send_message(message.from_user.id, data_dict.get("Error"))
        else:
            await bot.send_message(message.from_user.id, 'Тех неполадки')
        # except:
        #     await bot.send_message(message.from_user.id, "Извините, почему то нет связи, попробуйте позднее.")
    # await message.answer("Текст " + login)


# @dp.message_handler(state=login_save.login_actions, text="Изменить порог")
# async def func1(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         login = data["login"]
#         await login_save.new_limit.set()
#         await message.reply('Введите новый лимит порога')

@dp.message_handler(state=login_save.login_actions, text="Пополнить баланс")
async def func1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        login = data["login"]
        parm2 = {"Type": "GetPaymentLink", "Token": "", "Login": login, "TgId": message.from_user.id}
        try:
            response = requests.get('', params=parm2, verify=False,
                                    timeout=10)
            json_data = response.text
            data_dict = json.loads(json_data)
            if data_dict.get('Status') == 'Success':
                # await bot.send_message(message.from_user.id, json.loads(json_data))
                oplata = data_dict.get('Data').get('PaymentLink')
                # await bot.send_message(message.from_user.id, oplata)
                await bot.send_message(message.from_user.id,"Ссылка на оплату обсуживания:\n" + ' ' + oplata)
                dkbb = [
                    [
                        # types.KeyboardButton(text="Изменить порог"),
                        types.KeyboardButton(text="Пополнить баланс"),
                        types.KeyboardButton(text="Уведомлять о снижении баланса")
                    ],
                    [
                        types.KeyboardButton(text="Вернутся в меню")
                    ]
                ]
                markup = types.ReplyKeyboardMarkup(keyboard=dkbb, resize_keyboard=True)
                await message.answer("Выберите действие:", reply_markup=markup)
                await login_save.login_actions.set()
            elif data_dict.get('Status') == 'Error':
                # await bot.send_message(message.from_user.id, json.loads(json_data))
                await bot.send_message(message.from_user.id, 'Ошибка')
            else:
                await bot.send_message(message.from_user.id, 'Тех неполадки')
        except:
            await bot.send_message(message.from_user.id, "Извините, почему то нет связи, попробуйте позднее.")



# @dp.message_handler(state=login_save.new_limit)
# async def func1(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         login = data["login"]
#         log_lim = message.text
#         parm2 = {"Type": "SetLimit", "Token": "", "TgId": message.from_user.id, "Login": login, "Limit": log_lim}
#         try:
#             response = requests.get('', params=parm2, verify=False,
#                                     timeout=10)
#             json_data = response.text
#             data_dict = json.loads(json_data)
#             if data_dict.get('Status') == 'Success':
#                 # await bot.send_message(message.from_user.id, json.loads(json_data))
#                 # loginss = data_dict.get('Data').get('BindedList')
#                 await message.answer("Порог информирования успешно изменен!")
#                 bkb = [
#                     [
#                         types.KeyboardButton(text="Проверка баланса"),
#                         types.KeyboardButton(text="Слежение"),
#                     ],
#                     [
#                         types.KeyboardButton(text="Вернутся в меню")
#                     ]
#                 ]
#                 markup = types.ReplyKeyboardMarkup(keyboard=bkb, resize_keyboard=True)
#                 await message.answer("Выберите действие", reply_markup=markup)
#                 await login_save.login_actions.set()
#             elif data_dict.get('Status') == 'Error':
#                 await bot.send_message(message.from_user.id, 'Ошибка')
#             else:
#                 await bot.send_message(message.from_user.id, 'Тех неполадки')
#         except:
#             await bot.send_message(message.from_user.id, "Извините, почему то нет связи, попробуйте позднее.")


@dp.message_handler(state=login_save.login_actions, text="Вернутся в меню")
async def func1(message: types.Message, state: FSMContext):
    kb = [
        [
            types.KeyboardButton(text="Выбор логина"),
            types.KeyboardButton(text="Настройка логинов"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer("Выберите необходимое Вам действие из меню.",reply_markup=keyboard)
    await state.finish()


class login_save_del(StatesGroup):
    login_actions_del = State()


@dp.message_handler(text=['Отвязать логин'])
async def send_welcome(message: types.Message):
    parm = {"Type": "BindedList", "Token": "", "TgId": message.from_user.id}
    try:
        response = requests.get('', params=parm, verify=False, timeout=10)
        json_data = response.text
        data_dict = json.loads(json_data)
        if data_dict.get('Status') == 'Success':
            # await bot.send_message(message.from_user.id, json.loads(json_data))
            loginss = data_dict.get('Data').get('BindedList')
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for lgg in loginss:
                login = lgg.get('Login')
                descrip = lgg.get('Description')
                keyboard.add(types.InlineKeyboardButton(text=descrip, callback_data=f"delete_login:{login}"))
            await message.answer("Логины которые привязаны к вашему Telegram", reply_markup=keyboard)
        elif data_dict.get('Status') == 'Error':
            await bot.send_message(message.from_user.id, 'Ошибка')
        else:
            await bot.send_message(message.from_user.id, 'Тех неполадки')
    except:
        await bot.send_message(message.from_user.id, "Извините, почему то нет связи, попробуйте позднее.")

@dp.callback_query_handler(lambda c: c.data.startswith("delete_login:"))
async def send_random_value(call: types.CallbackQuery, state: FSMContext):
    cb = call.data.split()
    login = cb[0][13:]
    # desc = cb[1][12:]
    await call.message.answer(f"Вы выбрали:\nЛогин: {login}")
    await login_save_del.login_actions_del.set()
    async with state.proxy() as data:
        data["login"] = login

    bkb = [
        [
            types.KeyboardButton(text="Подтвердить отвязку логина"),
        ],
        [
            types.KeyboardButton(text="Вернутся в меню")
        ]
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=bkb, resize_keyboard=True)

    await call.message.answer("Выберите действие:", reply_markup=markup)


@dp.message_handler(state=login_save_del.login_actions_del, text="Подтвердить отвязку логина")
async def func1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        login = data["login"]
        # descrip = data["Description"]
        parm3 = {"Type": "UnBindLogin", "Token": "", "Login": login, "TgId": message.from_user.id}
        # await bot.send_message(message.from_user.id, parm3)
        try:
            response = requests.get('', params=parm3, verify=False,
                                    timeout=10)
            json_data = response.text
            data_dict = json.loads(json_data)
            # await bot.send_message(message.from_user.id, json.loads(json_data))
            if data_dict.get('Status') == 'Success':
                # await bot.send_message(message.from_user.id, json.loads(json_data))
                await bot.send_message(message.from_user.id, f'Логин {login} успешно отвязан от вашего Telegram')
                dkb = [
                    [
                        types.KeyboardButton(text="Привязать логин"),
                        types.KeyboardButton(text="Отвязать логин"),
                        types.KeyboardButton(text="Изменить название")
                    ],
                    [
                        types.KeyboardButton(text="Вернутся в меню")
                    ]
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=dkb, resize_keyboard=True)
                await message.reply("Выберете действие:", reply_markup=keyboard)
                await state.finish()
            elif data_dict.get('Status') == 'Error':
                await bot.send_message(message.from_user.id, 'Ошибка отвязки логина')
            else:
                await bot.send_message(message.from_user.id, 'Тех неполадки')
        except:
            await bot.send_message(message.from_user.id, "Извините, почему то нет связи, попробуйте позднее.")

@dp.message_handler(state=login_save_del.login_actions_del, text="Вернутся в меню")
async def func1(message: types.Message, state: FSMContext):
    dkb = [
            [
            types.KeyboardButton(text="Привязать логин"),
            types.KeyboardButton(text="Отвязать логин"),
            types.KeyboardButton(text="Изменить название")
          ],
        [
            types.KeyboardButton(text="Вернутся в меню")
        ]
        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=dkb, resize_keyboard=True)
    await message.reply("Выберете действие:", reply_markup=keyboard)
    await state.finish()



class login_save_rename(StatesGroup):
    login_actions_rename = State()
    new_name_rename = State()


@dp.message_handler(text=['Изменить название'])
async def cmd_dialog(message: types.Message):
    parm = {"Type": "BindedList", "Token": "", "TgId": message.from_user.id}
    try:
        response = requests.get('', params=parm, verify=False, timeout=10)
        json_data = response.text
        data_dict = json.loads(json_data)
        if data_dict.get('Status') == 'Success':
            # await bot.send_message(message.from_user.id, json.loads(json_data))
            loginss = data_dict.get('Data').get('BindedList')
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for lgg in loginss:
                login = lgg.get('Login')
                descrip = lgg.get('Description')
                keyboard.add(types.InlineKeyboardButton(text=descrip, callback_data=f"change_login:{login}"))
            await message.answer("Выберите логин для изменения названия", reply_markup=keyboard)
        elif data_dict.get('Status') == 'Error':
            await bot.send_message(message.from_user.id, 'Ошибка')
        else:
            await bot.send_message(message.from_user.id, 'Тех неполадки')
    except:
        await bot.send_message(message.from_user.id, "Извините, почему то нет связи, попробуйте позднее.")


@dp.callback_query_handler(lambda c: c.data.startswith("change_login:"))
async def send_value(call: types.CallbackQuery, state: FSMContext):
    cb = call.data.split()
    login = cb[0][13:]
    # desc = cb[1][12:]
    await call.message.answer(f"Вы выбрали:\nЛогин: {login}")
    # await call.message.answer(login)
    async with state.proxy() as data:
        data["login"] = login

    bkbk = [
        [
            types.KeyboardButton(text="Вернутся в меню")
        ]
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=bkbk, resize_keyboard=True)

    await call.message.answer("Введите новое название:", reply_markup=markup)
    await login_save_rename.login_actions_rename.set()

    # await get_answer.login_add.set()
    # await message.reply('Выберите логин для изменения названия')

@dp.message_handler(state=login_save_rename.login_actions_rename)
async def func1(message: types.Message, state: FSMContext):
    if message.text == "Вернутся в меню":
        # await bot.send_message(message.from_user.id, f'Название недопустимо')
        await state.finish()
        dkb = [
            [
                types.KeyboardButton(text="Привязать логин"),
                types.KeyboardButton(text="Отвязать логин"),
                types.KeyboardButton(text="Изменить название")
            ],
            [
                types.KeyboardButton(text="Вернутся в меню")
            ]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=dkb, resize_keyboard=True)
        await message.reply("Выберете действие заново:", reply_markup=keyboard)
    else:
        async with state.proxy() as data:
            login = data["login"]
        description = message.text
        # await message.answer(f"Новое название - {description}")
        parm4 = {"Type": "SetLoginDescription", "Token": "", "TgId": message.from_user.id,
                 "Login": login, "Description": description}
        # await bot.send_message(message.from_user.id, parm4)
        try:
            response = requests.get('', params=parm4, verify=False,
                                    timeout=10)
            json_data = response.text
            data_dict = json.loads(json_data)
            # await bot.send_message(message.from_user.id, json.loads(json_data))
            if data_dict.get('Status') == 'Success':
                # await bot.send_message(message.from_user.id, json.loads(json_data))
                await bot.send_message(message.from_user.id, f'Название изменено')
                dkb = [
                    [
                        types.KeyboardButton(text="Привязать логин"),
                        types.KeyboardButton(text="Отвязать логин"),
                        types.KeyboardButton(text="Изменить название")
                    ],
                    [
                        types.KeyboardButton(text="Вернутся в меню")
                    ]
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=dkb, resize_keyboard=True)
                await message.reply("Выберете действие:", reply_markup=keyboard)
                await state.finish()
            elif data_dict.get('Status') == 'Error':
                # await bot.send_message(message.from_user.id, json.loads(json_data))

                await bot.send_message(message.from_user.id, 'Ошибка изменения названия')
            else:
                await bot.send_message(message.from_user.id, 'Тех неполадки')
        except:
            await bot.send_message(message.from_user.id, "Извините, почему то нет связи, попробуйте позднее.")
        await state.finish()

@dp.message_handler(state=login_save_rename.login_actions_rename, text="Вернутся в меню")
async def func1(message: types.Message, state: FSMContext):
    dkb = [
            [
            types.KeyboardButton(text="Привязать логин"),
            types.KeyboardButton(text="Отвязать логин"),
            types.KeyboardButton(text="Изменить название")
          ],
        [
            types.KeyboardButton(text="Вернутся в меню")
        ]
        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=dkb, resize_keyboard=True)
    await message.reply("Выберете действие:", reply_markup=keyboard)
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)

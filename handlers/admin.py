import aiogram
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from data_base import sqlite_db, sqlite_db_chanall, tech_db
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers import oplata
import os
from dotenv import load_dotenv


load_dotenv()


TARGET_USER_ID = int(os.getenv("VLAD"))


class FSMChanall(StatesGroup):
    id_chanal = State()
    chanal = State()
    tarif = State()
    price = State()
    selected_tariffs = State()
    text_selected =State()


class FSMAdmin(StatesGroup):
    reject_reason = State()


class FSMAns(StatesGroup):
    id_tech = State()
    answer = State()


@dp.message_handler(text=["Администратор"])
async def cmd_start_admin(message: types.Message):
    if message.from_user.id == TARGET_USER_ID:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="Показать запросы на рекламу", callback_data="show_new_rows"))
        keyboard.add(InlineKeyboardButton(text="Посмотреть новые записи тех.поддержки", callback_data="show_new_tech"))
        keyboard.add(InlineKeyboardButton(text="Добавить канал", callback_data="add_new_chanall"))
        keyboard.row(InlineKeyboardButton(text="Удалить канал", callback_data="delete_new_chanall"))
        await message.answer("Админское меню", reply_markup=keyboard)
    else:
        await message.answer("Вы не являетесь администратором")

result = 0


@dp.callback_query_handler(text="show_new_tech", state="*")
async def show_new_tech(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    global result
    result1 = await tech_db.sql_all()
    print(result1)
    result1 = result1[0][0]
    if result != result1:
        score = result1 - result
        tech = await tech_db.sql_read(score)
        print(tech)
        sent_users = set()
        for tech_elm in tech:
            user_id = tech_elm[1]
            if user_id not in sent_users:
                message_text = f'\nПользователь:{user_id}'
                a = await tech_db.sql_old(user_id)
                if len(a) >= 1:
                    for a_elm in a:
                        message_text += f'\n<b>Обращение {a_elm[2]}:</b>\n{a_elm[0]}\n<b>Ответ:</b>\n{a_elm[1]}\n'
                admin_chat_id = 819074198  # ID чата администратора
                await bot.send_message(
                    chat_id=admin_chat_id,
                    text=message_text,
                    parse_mode=aiogram.types.ParseMode.HTML,
                    reply_markup=await get_answer_keyboard(tech_elm[0], user_id, tech_elm[2])
                )
                sent_users.add(user_id)
        result = result1
    else:
        await bot.send_message(chat_id=819074198, text="Новых строк нету")


async def get_answer_keyboard(id_tech,user_id, tech):
    keyboard = InlineKeyboardMarkup()
    answer_data = f"answer_{user_id}_{tech}_{id_tech}"
    keyboard.add(InlineKeyboardButton(text="Ответить на:", callback_data=answer_data))
    return keyboard


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("answer_"), state="*")
async def answer_row(callback_query: types.CallbackQuery, state: FSMContext):
    row_id = callback_query.data.split("_")[1]
    row_tech = callback_query.data.split("_")[2]
    row_id_tech = callback_query.data.split("_")[3]
    await bot.send_message(chat_id=callback_query.message.chat.id, text=f'Введите ваш ответ на вопрос:{row_tech}')
    async with state.proxy() as data:
        data['id_tech'] = row_id_tech
    await FSMAns.answer.set()
    await state.update_data(row_id=row_id)


@dp.message_handler(state=FSMAns.answer)
async def process_answer_reason(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        row_id = data['row_id']
        answer = message.text
        await tech_db.sql_add_answer(data['id_tech'], answer)
    await bot.send_message(chat_id=row_id, text=f'Администратор ответил на ваш запрос. Ответ:\n {answer}')
    await state.finish()


post_data = {}

@dp.callback_query_handler(text="show_new_rows", state="*")
async def show_new_rows(callback_query: types.CallbackQuery, state: FSMContext):
    post_id = 0
    await callback_query.answer()
    global result
    result1 = await sqlite_db.sql_all()
    print(result1)
    result1 = result1[0][0]
    if result != result1:
        score = result1 - result
        ret = await sqlite_db.sql_read(score)
        print(ret)
        for ret_elm in ret:
            post_id += 1
            user_id_for_payment = ret_elm[1]
            chanall_for_payment = ret_elm[2]
            tariff_for_payment = ret_elm[3]
            date_for_payment = ret_elm[4]
            text_for_payment = ret_elm[5]
            photo_for_payment = ret_elm[6]
            formatted_text = ret_elm[5]
            photo_file_id = ret_elm[6]
            post_data[post_id] = {
                'user_id_for_payment': user_id_for_payment,
                'chanall_for_payment': chanall_for_payment,
                'tariff_for_payment': tariff_for_payment,
                'date_for_payment': date_for_payment,
                'text_for_payment': text_for_payment,
                'photo_for_payment': photo_for_payment,
            }
            if photo_file_id:
                await bot.send_photo(819074198, photo=photo_file_id, caption=formatted_text, parse_mode=aiogram.types.ParseMode.HTML, reply_markup=await get_approval_keyboard(post_id, chanall_for_payment, tariff_for_payment))
            else:
                await bot.send_message(819074198, formatted_text, parse_mode=aiogram.types.ParseMode.HTML, reply_markup=await get_approval_keyboard(post_id, chanall_for_payment, tariff_for_payment))
            result = result1
    else:
        await bot.send_message(chat_id=819074198, text="Новых строк нету")


async def get_approval_keyboard(user_id, channel, tariff):
    print('admin_kb')
    print(user_id, channel, tariff)
    keyboard = InlineKeyboardMarkup()
    approve_data = f"approve_{user_id}_{channel}_{tariff}"
    reject_data = f"reject_{user_id}_{channel}_{tariff}"
    keyboard.add(InlineKeyboardButton(text="Одобрить", callback_data=approve_data))
    keyboard.add(InlineKeyboardButton(text="Отклонить", callback_data=reject_data))
    return keyboard


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("approve_"))
async def approve_row(callback_query: types.CallbackQuery):
    print('aapro')
    post_id = int(callback_query.data.split("_")[1])
    print(post_id)
    print(post_data)
    if post_id in post_data:
        post = post_data[post_id]
        user_id_for_payment = post['user_id_for_payment']
        chanall_for_payment = post['chanall_for_payment']
        tariff_for_payment = post['tariff_for_payment']
        date_for_payment = post['date_for_payment']
        text_for_payment = post['text_for_payment']
        photo_for_payment = post['photo_for_payment']
        b5 = InlineKeyboardButton(text='ЮКасса', callback_data=f'money_1_{post_id}')
        b6 = InlineKeyboardButton(text='Криптовалюта', callback_data=f'money_2_{post_id}')
        check_opl = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(b5, b6)
        print(user_id_for_payment, chanall_for_payment, tariff_for_payment, date_for_payment, text_for_payment, photo_for_payment)
        await bot.send_message(chat_id=user_id_for_payment, text='Выберите способ оплаты:',reply_markup=check_opl)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("money_"), state="*")
async def reject_row(callback_query: types.CallbackQuery, state: FSMContext):
    post_id = int(callback_query.data.split("_")[2])
    check_opl = int(callback_query.data.split("_")[1])
    if post_id in post_data:
        post = post_data[post_id]
        user_id_for_payment = post['user_id_for_payment']
        chanall_for_payment = post['chanall_for_payment']
        tariff_for_payment = post['tariff_for_payment']
        date_for_payment = post['date_for_payment']
        text_for_payment = post['text_for_payment']
        photo_for_payment = post['photo_for_payment']
        if check_opl == 1:
            await oplata.send_invoice(user_id_for_payment, chanall_for_payment, tariff_for_payment,
                                      date_for_payment, text_for_payment, photo_for_payment, 2)
        else:
            b5 = InlineKeyboardButton(text='USDT', callback_data=f'val_USDT_{post_id}')
            b6 = InlineKeyboardButton(text='TON', callback_data=f'val_TON_{post_id}')
            b7 = InlineKeyboardButton(text='BTC', callback_data=f'val_BTC_{post_id}')
            b8 = InlineKeyboardButton(text='ETH', callback_data=f'val_ETH_{post_id}')
            b9 = InlineKeyboardButton(text='BNB', callback_data=f'val_BNB_{post_id}')
            b10 = InlineKeyboardButton(text='BUSD', callback_data=f'val_BUSD_{post_id}')
            check_val = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(b5, b6, b7).row(b8, b9, b10)
            await bot.send_message(chat_id=user_id_for_payment, text='Выберите валюту:', reply_markup=check_val)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("val_"), state="*")
async def reject_row(callback_query: types.CallbackQuery, state: FSMContext):
    post_id = int(callback_query.data.split("_")[2])
    check_valute = callback_query.data.split("_")[1]
    if post_id in post_data:
        post = post_data[post_id]
        user_id_for_payment = post['user_id_for_payment']
        chanall_for_payment = post['chanall_for_payment']
        tariff_for_payment = post['tariff_for_payment']
        date_for_payment = post['date_for_payment']
        text_for_payment = post['text_for_payment']
        photo_for_payment = post['photo_for_payment']
        await oplata.crypto(user_id_for_payment, chanall_for_payment, tariff_for_payment,
                                  date_for_payment, text_for_payment, photo_for_payment, check_valute)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("reject_"), state="*")
async def reject_row(callback_query: types.CallbackQuery, state: FSMContext):
    post_id = int(callback_query.data.split("_")[1])
    if post_id in post_data:
        post = post_data[post_id]
        user_id_for_payment = post['user_id_for_payment']
        await bot.send_message(chat_id=callback_query.message.chat.id, text='Введите причину отклонения:')
        await FSMAdmin.reject_reason.set()
        await state.update_data(user_id_for_payment=user_id_for_payment)


@dp.message_handler(state=FSMAdmin.reject_reason)
async def process_reject_reason(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id_for_payment = data['user_id_for_payment']
        reason = message.text
        await bot.send_message(chat_id=user_id_for_payment, text=f'Вашу запись не одобрили. Причина: {reason}')
        await state.finish()


chats = {}


@dp.my_chat_member_handler()
async def add_bot_channel(event: types.ChatMemberUpdated):
    global chats
    if event.new_chat_member.status == 'administrator':
        chat_id = event.chat.id
        chat_title = event.chat.title
        chats[chat_id] = chat_title


@dp.callback_query_handler(text="add_new_chanall", state="*")
async def add_new_chanall(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard_c = types.InlineKeyboardMarkup(row_width=1)
    for chat_id, chat_title in chats.items():
        keyboard_c.add(InlineKeyboardButton(text=chat_title, callback_data=f"chanal_{chat_id}_{chat_title}"))
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите канал:', reply_markup=keyboard_c)
    print(chats.items())
    await FSMChanall.chanal.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("chanal_"), state="*")
async def process_channel_callback(callback_query: types.CallbackQuery, state: FSMContext):
    print("Яхаааа бля")
    channel_id = callback_query.data.split('_')[1]
    channel_title = callback_query.data.split('_')[2]
    print(channel_id)
    async with state.proxy() as data:
        data['id_chanal'] = channel_id
        data['chanal'] = channel_title
        data['selected_tariffs'] = []
        data['prices'] = []
        print(data)
        keyboard = get_tariff_keyboard()
        await bot.send_message(chat_id=callback_query.message.chat.id, text='Теперь введите тарифы',
                               reply_markup=keyboard)
        await FSMChanall.tarif.set()


def get_tariff_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    tariffs = ["На день", "На 2 дня", "На неделю", "На месяц"]
    for tariff in tariffs:
        keyboard.add(InlineKeyboardButton(text=tariff, callback_data=f"tariff_{tariff}"))
    keyboard.add(InlineKeyboardButton(text="Далее", callback_data="next_to_price"))
    return keyboard


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("tariff_"), state=FSMChanall.tarif)
async def process_tariff_selection(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        selected_tariffs = data.get('selected_tariffs', [])
        tariff = callback_query.data.split("_")[1]
        if tariff not in selected_tariffs:
            selected_tariffs.append(tariff)
        data['selected_tariffs'] = selected_tariffs


@dp.callback_query_handler(lambda callback_query: callback_query.data == "next_to_price", state=FSMChanall.tarif)
async def next_to_price(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        selected_tariffs = data.get('selected_tariffs', [])
        if selected_tariffs:
            selected_tariffs_text = ', '.join(selected_tariffs)
            data['text_selected'] = selected_tariffs_text
            data['current_tariff_index'] = 0
            await bot.send_message(
                callback_query.message.chat.id,
                f'Выбранные тарифы: {selected_tariffs_text}\n\n'
                f'Теперь введите цену для тарифа "{selected_tariffs[0]}":'
            )
            await FSMChanall.price.set()
        else:
            await bot.send_message(callback_query.message.chat.id, 'Вы не выбрали ни одного тарифа. Выберите тарифы и затем введите цену:')


@dp.message_handler(state=FSMChanall.price)
async def process_channel_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        id_chanal = data['id_chanal']
        chanal = data['chanal']
        selected_tariffs = data.get('selected_tariffs', [])
        current_tariff_index = data.get('current_tariff_index', 0)
        prices = data.get('prices', [])
        if current_tariff_index < len(selected_tariffs):
            tariff = selected_tariffs[current_tariff_index]
            price = message.text.strip()
            prices.append((tariff, price))
            current_tariff_index += 1
            data['current_tariff_index'] = current_tariff_index
            data['prices'] = prices
            if current_tariff_index < len(selected_tariffs):
                next_tariff = selected_tariffs[current_tariff_index]
                await bot.send_message(
                    message.chat.id,
                    f'Введите цену для тарифа "{next_tariff}":'
                )
            else:
                prices_string = '/'.join([f'{tariff}={price}' for tariff, price in prices])
                await bot.send_message(
                    message.chat.id,
                    f'Цены для всех выбранных тарифов сохранены.'
                )
                await sqlite_db_chanall.add_ch(id_chanal, chanal, data['text_selected'], prices_string)
                await clear_price_data(state)
                print('Добавлен')
                await state.finish()
        else:
            await bot.send_message(
                message.chat.id,
                f'Все цены уже введены. Если хотите изменить цену, выберите другой тариф и начните вводить цены заново.'
            )


async def clear_price_data(state: FSMContext):
    async with state.proxy() as data:
        data.pop('prices', None)


@dp.callback_query_handler(text="delete_new_chanall", state="*")
async def delete_new_chanall(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Выберите канал, который нужно удалить")
    all_ch = sqlite_db_chanall.all_ch()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for elem in all_ch:
        channel_name = elem[1]
        delete_button = types.InlineKeyboardButton(
            f"Удалить канал {channel_name}", callback_data=f"delete_channel:{elem[0]}"
        )
        keyboard.add(delete_button)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Список каналов:", reply_markup=keyboard)



@dp.callback_query_handler(lambda c: c.data.startswith("delete_channel:"))
async def delete_channel(callback_query: types.CallbackQuery, state: FSMContext):
    channel_id = callback_query.data.split(":")[1]
    sqlite_db_chanall.delete_ch(channel_id)
    await bot.send_message(chat_id=callback_query.message.chat.id, text=f'Канал "{channel_id}" удален')


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("reject_"), state="*")
async def reject_row(callback_query: types.CallbackQuery, state: FSMContext):
    post_id = int(callback_query.data.split("_")[1])
    if post_id in post_data:
        post = post_data[post_id]
        user_id_for_payment = post['user_id_for_payment']
        await bot.send_message(chat_id=callback_query.message.chat.id, text='Введите причину отклонения:')
        await FSMAdmin.reject_reason.set()
        await state.update_data(user_id_for_payment=user_id_for_payment)


@dp.message_handler(state=FSMAdmin.reject_reason)
async def process_reject_reason(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id_for_payment = data['user_id_for_payment']
        reason = message.text
        await bot.send_message(chat_id=user_id_for_payment, text=f'Вашу запись не одобрили. Причина: {reason}')
        await state.finish()



